import re
from werkzeug.utils import secure_filename


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename to only allow safe characters."""
    filename = secure_filename(filename)
    # Extra: only allow a-z0-9._-
    filename = re.sub(r'[^a-zA-Z0-9._\-]', '_', filename)
    return filename[:200]  # Limit length
