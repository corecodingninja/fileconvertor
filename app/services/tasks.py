import os
from datetime import datetime
from app import celery, db
from app.models.conversion import ConversionJob
from app.models.usage_stat import DailyStat
from app.services.converter import (
    convert_word_to_pdf, convert_pdf_to_word,
    convert_image, compress_image
)
from app.services.file_handler import cleanup_expired_jobs


@celery.task(bind=True, max_retries=2)
def run_conversion(self, job_id: str):
    """Main Celery task: run file conversion for a job."""
    job = ConversionJob.query.get(job_id)
    if not job:
        return

    job.status = 'processing'
    db.session.commit()

    start_time = datetime.utcnow()
    output_dir = os.path.dirname(job.input_path)

    try:
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
        elif job.type == 'image_to_bmp':
            output_path = convert_image(job.input_path, output_dir, 'BMP')
        elif job.type == 'image_to_tiff':
            output_path = convert_image(job.input_path, output_dir, 'TIFF')
        elif job.type == 'image_to_gif':
            output_path = convert_image(job.input_path, output_dir, 'GIF')
        elif job.type == 'compress_image':
            output_path = compress_image(job.input_path, output_dir)
        else:
            raise ValueError(f"Unknown conversion type: {job.type}")

        job.output_path = output_path
        job.status = 'done'
        job.completed_at = datetime.utcnow()

        # Update daily stats
        elapsed_ms = int((job.completed_at - start_time).total_seconds() * 1000)
        _update_stats(job.type, job.file_size_bytes or 0, elapsed_ms, failed=False)

    except Exception as exc:
        job.status = 'failed'
        job.error_message = str(exc)[:500]
        job.completed_at = datetime.utcnow()
        _update_stats(job.type, 0, 0, failed=True)

    db.session.commit()


@celery.task
def cleanup_expired():
    """Periodic task: delete expired job files."""
    count = cleanup_expired_jobs()
    return f'Cleaned up {count} expired jobs'


def _update_stats(job_type: str, size_bytes: int, elapsed_ms: int, failed: bool):
    try:
        stat = DailyStat.get_or_create_today()
        if not failed:
            if job_type == 'word_to_pdf':
                stat.word_to_pdf_count = (stat.word_to_pdf_count or 0) + 1
            elif job_type == 'pdf_to_word':
                stat.pdf_to_word_count = (stat.pdf_to_word_count or 0) + 1
            else:
                stat.image_conversion_count = (stat.image_conversion_count or 0) + 1
            
            stat.total_bytes_processed = (stat.total_bytes_processed or 0) + size_bytes
            # Rolling average
            total_jobs = (stat.word_to_pdf_count or 0) + (stat.pdf_to_word_count or 0) + (stat.image_conversion_count or 0)
            prev_avg = stat.avg_conversion_ms or 0
            stat.avg_conversion_ms = int(
                (prev_avg * (total_jobs - 1) + elapsed_ms) / total_jobs
            )
        else:
            stat.failure_count = (stat.failure_count or 0) + 1
        db.session.commit()
    except Exception:
        pass
