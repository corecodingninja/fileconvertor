import os
import subprocess
import shutil
from pathlib import Path
from PIL import Image


def convert_word_to_pdf(input_path: str, output_dir: str) -> str:
    """Convert a Word document to PDF using LibreOffice headless.
    Returns path to output PDF file.
    """
    binary = _ensure_libreoffice()
    cmd = [
        binary, '--headless', '--convert-to', 'pdf',
        '--outdir', output_dir, input_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f'LibreOffice conversion failed: {result.stderr}')

    # LibreOffice names output as <input_stem>.pdf
    stem = Path(input_path).stem
    output_path = os.path.join(output_dir, f'{stem}.pdf')
    if not os.path.exists(output_path):
        raise FileNotFoundError(f'Expected output file not found: {output_path}')
    return output_path


def convert_image(input_path: str, output_dir: str, target_format: str) -> str:
    """Convert an image to target format using Pillow.
    target_format should be 'JPEG', 'PNG', 'WEBP', etc.
    """
    stem = Path(input_path).stem
    ext = target_format.lower()
    if ext == 'jpeg':
        ext = 'jpg'
    output_path = os.path.join(output_dir, f'{stem}.{ext}')

    with Image.open(input_path) as img:
        # Convert to RGB if saving as JPEG (avoids transparency issues)
        if target_format.upper() in ('JPEG', 'JPG') and img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')
        img.save(output_path, target_format.upper())

    return output_path


def compress_image(input_path: str, output_dir: str, quality: int = 65) -> str:
    """Compress an image using Pillow. Returns path to compressed file."""
    stem = Path(input_path).stem
    suffix = Path(input_path).suffix
    output_path = os.path.join(output_dir, f'{stem}_compressed{suffix}')

    with Image.open(input_path) as img:
        orig_format = img.format or 'JPEG'
        
        # Convert RGBA/P/LA images with RGB suffix to RGB
        if img.mode in ('RGBA', 'P', 'LA') and suffix.lower() in ('.jpg', '.jpeg'):
            img = img.convert('RGB')
            orig_format = 'JPEG'
        
        # Build save parameters based on format
        save_params = {}
        
        if orig_format in ('JPEG', 'JPG'):
            save_params['quality'] = quality
            save_params['optimize'] = True
        elif orig_format == 'PNG':
            save_params['optimize'] = True
            save_params['compress_level'] = 9
        elif orig_format == 'WEBP':
            save_params['quality'] = quality
            save_params['method'] = 6  # Highest compression method
        elif orig_format == 'GIF':
            save_params['optimize'] = True
        
        img.save(output_path, format=orig_format, **save_params)

    return output_path


def convert_pdf_to_word(input_path: str, output_dir: str) -> str:
    """Convert a PDF to DOCX using pdf2docx library.
    Returns path to output DOCX file.
    """
    from pdf2docx import Converter
    stem = Path(input_path).stem
    output_path = os.path.join(output_dir, f'{stem}.docx')
    
    cv = Converter(input_path)
    cv.convert(output_path, start=0, multi_processing=False)
    cv.close()
    
    if not os.path.exists(output_path):
        raise FileNotFoundError(f'Failed to generate DOCX file: {output_path}')
    return output_path


def _ensure_libreoffice() -> str:
    """Find LibreOffice binary (soffice) across different platforms.
    Returns the command/path to use.
    """
    # 1. Check PATH
    for cmd in ['libreoffice', 'soffice']:
        if shutil.which(cmd):
            return cmd

    # 2. Check common macOS locations
    mac_paths = [
        '/Applications/LibreOffice.app/Contents/MacOS/soffice',
        '/usr/local/bin/soffice',
        '/opt/homebrew/bin/soffice',
    ]
    for path in mac_paths:
        if os.path.exists(path):
            return path

    # 3. If not found, raise helpful error
    raise EnvironmentError(
        'LibreOffice (soffice) not found. '
        'On macOS: Please install from libreoffice.org. '
        'On Linux: sudo apt-get install -y libreoffice'
    )
