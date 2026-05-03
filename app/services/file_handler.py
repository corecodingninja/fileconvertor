import os
import shutil
from datetime import datetime, timedelta
from flask import current_app
from app.utils.sanitizer import sanitize_filename


def get_upload_folder() -> str:
    folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(folder, exist_ok=True)
    return folder


def save_uploaded_file(file, job_id: str) -> tuple[str, int]:
    """Save uploaded file to temp storage. Returns (path, size_bytes)."""
    folder = get_upload_folder()
    safe_name = sanitize_filename(file.filename)
    job_folder = os.path.join(folder, job_id)
    os.makedirs(job_folder, exist_ok=True)
    input_path = os.path.join(job_folder, f'input_{safe_name}')
    file.save(input_path)
    size = os.path.getsize(input_path)
    return input_path, size


def cleanup_job_files(job_id: str):
    """Delete all files associated with a job."""
    folder = current_app.config['UPLOAD_FOLDER']
    job_folder = os.path.join(folder, job_id)
    if os.path.exists(job_folder):
        shutil.rmtree(job_folder)


def cleanup_expired_jobs():
    """Called by Celery beat task — remove expired job files + update DB."""
    from app.models.conversion import ConversionJob
    from app import db
    now = datetime.utcnow()
    expired = ConversionJob.query.filter(
        ConversionJob.expires_at < now,
        ConversionJob.status.in_(['done', 'failed', 'pending'])
    ).all()
    for job in expired:
        try:
            cleanup_job_files(job.id)
        except Exception:
            pass
    return len(expired)
