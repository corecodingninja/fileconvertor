import os
import hashlib
from flask import current_app


def validate_word_file(file):
    """Validate uploaded Word file. Returns (ok, error_message)."""
    if not file or file.filename == '':
        return False, 'No file selected.'

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in current_app.config['ALLOWED_WORD_EXTENSIONS']:
        return False, f'Invalid file type. Only .docx and .doc files are allowed.'

    # Read a bit to check MIME
    header = file.read(8)
    file.seek(0)

    # DOCX: PK zip signature; DOC: D0 CF 11 E0
    if not (header[:2] == b'PK' or header[:8] == b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'):
        return False, 'File content does not match a valid Word document.'

    return True, None


def validate_pdf_file(file):
    """Validate uploaded PDF file. Returns (ok, error_message)."""
    if not file or file.filename == '':
        return False, 'No file selected.'

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in current_app.config['ALLOWED_PDF_EXTENSIONS']:
        return False, 'Invalid file type. Only .pdf files are allowed.'

    header = file.read(5)
    file.seek(0)

    if header != b'%PDF-':
        return False, 'File content does not match a valid PDF.'

    return True, None


def validate_image_file(file):
    """Validate uploaded Image file. Returns (ok, error_message)."""
    if not file or file.filename == '':
        return False, 'No file selected.'

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in current_app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return False, f"Invalid file type. Allowed: {', '.join(current_app.config['ALLOWED_IMAGE_EXTENSIONS'])}"

    # Basic header check for common images
    header = file.read(12)
    file.seek(0)

    # PNG: 89 50 4E 47 0D 0A 1A 0A
    # JPEG: FF D8 FF
    # WebP: RIFF .... WEBP
    is_png = header[:8] == b'\x89PNG\r\n\x1a\n'
    is_jpg = header[:3] == b'\xff\xd8\xff'
    is_webp = header[:4] == b'RIFF' and header[8:12] == b'WEBP'
    
    if not (is_png or is_jpg or is_webp):
        # Fallback to just extension for less common ones like .bmp
        if ext not in ('.bmp'):
            return False, 'File content does not match a valid image format.'

    return True, None


def hash_ip(ip: str) -> str:
    """SHA-256 hash an IP address for privacy-safe storage."""
    return hashlib.sha256(ip.encode()).hexdigest()
