import os
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file, current_app
from app import db, limiter
from app.models.conversion import ConversionJob
from app.utils.validators import validate_word_file, validate_pdf_file, validate_image_file, hash_ip
from app.services.file_handler import save_uploaded_file

api_bp = Blueprint('api', __name__)


def is_worker_running():
    """Check if at least one Celery worker is active."""
    try:
        from app import celery
        # Timeout quickly if no response
        inspect = celery.control.inspect(timeout=0.5)
        stats = inspect.stats()
        return stats is not None and len(stats) > 0
    except Exception:
        return False


def get_client_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr or '').split(',')[0].strip()


@api_bp.route('/convert', methods=['POST'])
@limiter.limit('10 per hour', key_func=get_client_ip)
def convert():
    """Upload file and start async conversion. Returns job_id."""
    conversion_type = request.form.get('type')
    file = request.files.get('file')

    allowed_types = (
        'word_to_pdf', 'pdf_to_word', 
        'png_to_jpg', 'jpg_to_png', 'image_to_webp', 'compress_image'
    )
    if conversion_type not in allowed_types:
        return jsonify({'error': 'Invalid conversion type.'}), 400

    # Validate
    if conversion_type == 'word_to_pdf':
        ok, err = validate_word_file(file)
    elif conversion_type == 'pdf_to_word':
        ok, err = validate_pdf_file(file)
    else:
        ok, err = validate_image_file(file)

    if not ok:
        return jsonify({'error': err}), 422

    # Check concurrent jobs
    ip = get_client_ip()
    hashed_ip = hash_ip(ip)
    active_jobs = ConversionJob.query.filter_by(
        ip_address=hashed_ip, status='processing'
    ).count()
    if active_jobs >= current_app.config.get('MAX_CONCURRENT_JOBS_PER_IP', 2):
        return jsonify({'error': 'Too many active conversions. Please wait.'}), 429

    # Create job
    job = ConversionJob(
        type=conversion_type,
        status='pending',
        original_filename=file.filename,
        ip_address=hashed_ip,
    )
    db.session.add(job)
    db.session.flush()  # get job.id

    # Save file
    try:
        input_path, size = save_uploaded_file(file, job.id)
        job.input_path = input_path
        job.file_size_bytes = size
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to save file.'}), 500

    # Queue Celery task or run synchronously
    use_celery = False
    try:
        if is_worker_running():
            from app.services.tasks import run_conversion
            run_conversion.delay(job.id)
            use_celery = True
            current_app.logger.info(f"Queued job {job.id} via Celery")
        else:
            current_app.logger.info(f"No Celery workers detected, using synchronous fallback for job {job.id}")
            _run_sync(job)
    except Exception as e:
        current_app.logger.warning(f"Error starting conversion: {e}. Falling back to sync.")
        _run_sync(job)

    return jsonify({'job_id': job.id, 'status': job.status}), 202


@api_bp.route('/status/<job_id>', methods=['GET'])
def status(job_id):
    """Poll conversion job status."""
    job = ConversionJob.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found.'}), 404
    return jsonify(job.to_dict()), 200


@api_bp.route('/download/<job_id>', methods=['GET'])
def download(job_id):
    """Download the converted file."""
    job = ConversionJob.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found.'}), 404
    if job.status != 'done':
        return jsonify({'error': 'File not ready.'}), 400
    if not job.output_path or not os.path.exists(job.output_path):
        return jsonify({'error': 'File has expired or was deleted.'}), 410

    # Mark downloaded
    job.downloaded_at = datetime.utcnow()
    db.session.commit()

    # Determine download filename
    import os as _os
    ext = _os.path.splitext(job.output_path)[1]
    stem = _os.path.splitext(job.original_filename)[0]
    download_name = f'{stem}{ext}'

    return send_file(
        job.output_path,
        as_attachment=True,
        download_name=download_name,
    )


@api_bp.route('/file/<job_id>', methods=['DELETE'])
def delete_file(job_id):
    """Manually delete job files."""
    job = ConversionJob.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found.'}), 404
    from app.services.file_handler import cleanup_job_files
    cleanup_job_files(job.id)
    job.status = 'failed'
    job.error_message = 'Manually deleted by user'
    db.session.commit()
    return jsonify({'deleted': True}), 200


def _run_sync(job):
    """Synchronous fallback conversion (when Celery/Redis not available)."""
    from app.services.converter import convert_word_to_pdf, convert_pdf_to_word
    import os
    
    current_app.logger.info(f"Starting synchronous conversion for job {job.id}")
    job.status = 'processing'
    db.session.commit()
    
    start = datetime.utcnow()
    output_dir = os.path.dirname(job.input_path)
    try:
        from app.services.converter import (
            convert_word_to_pdf, convert_pdf_to_word, 
            convert_image, compress_image
        )
        
        if job.type == 'word_to_pdf':
            output_path = convert_word_to_pdf(job.input_path, output_dir)
        elif job.type == 'pdf_to_word':
            output_path = convert_pdf_to_word(job.input_path, output_dir)
        elif job.type == 'png_to_jpg':
            output_path = convert_image(job.input_path, output_dir, 'JPEG')
        elif job.type == 'jpg_to_png':
            output_path = convert_image(job.input_path, output_dir, 'PNG')
        elif job.type == 'image_to_webp':
            output_path = convert_image(job.input_path, output_dir, 'WEBP')
        elif job.type == 'compress_image':
            output_path = compress_image(job.input_path, output_dir)
        else:
            raise ValueError(f"Unknown conversion type: {job.type}")
        
        job.output_path = output_path
        job.status = 'done'
        job.completed_at = datetime.utcnow()
        current_app.logger.info(f"Sync conversion done for job {job.id}")
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        current_app.logger.error(f"Sync conversion failed for job {job.id}:\n{error_trace}")
        job.status = 'failed'
        job.error_message = str(e)[:500]
        job.completed_at = datetime.utcnow()
    
    db.session.commit()
