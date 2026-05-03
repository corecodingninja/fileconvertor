import uuid
from datetime import datetime, timedelta
from app import db


class ConversionJob(db.Model):
    __tablename__ = 'conversion_jobs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = db.Column(
        db.Enum(
            'word_to_pdf', 'pdf_to_word', 
            'png_to_jpg', 'jpg_to_png', 'image_to_webp', 'compress_image',
            name='job_type'
        ), 
        nullable=False
    )
    status = db.Column(
        db.Enum('pending', 'processing', 'done', 'failed', name='job_status'),
        default='pending', nullable=False
    )
    original_filename = db.Column(db.String(255), nullable=False)
    file_size_bytes = db.Column(db.Integer)
    input_path = db.Column(db.Text)
    output_path = db.Column(db.Text)
    error_message = db.Column(db.Text)
    ip_address = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    downloaded_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10))

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'status': self.status,
            'original_filename': self.original_filename,
            'file_size_bytes': self.file_size_bytes,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
        }
