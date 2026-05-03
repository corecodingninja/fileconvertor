FROM python:3.12-slim

# Install system dependencies for LibreOffice and PDF conversion
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    python3-uno \
    libpangocairo-1.0-0 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for file storage
RUN mkdir -p /tmp/fileconverter && chmod 777 /tmp/fileconverter

# Expose port
EXPOSE 5001

# Start application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "run:app"]
