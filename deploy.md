# Deployment Guide — ConverterHub

ConverterHub is designed to be deployed on modern cloud platforms like Render, Heroku, or via Docker.

## 1. Quick Deploy (Render / Heroku)
- **Runtime**: Python 3.12+
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn run:app`
- **Environment Variables**:
  - `FLASK_ENV`: `production`
  - `SECRET_KEY`: A long random string
  - `DATABASE_URL`: (Optional) PostgreSQL URL
  - `REDIS_URL`: URL for Celery broker/backend
  - `ADSENSE_CLIENT`: Your Google AdSense ID (ca-pub-...)

## 2. Docker Deployment
We provide a `Dockerfile` that includes all system dependencies for LibreOffice.
```bash
docker build -t fileconverter .
docker run -p 5001:5001 -e SECRET_KEY=your_key fileconverter
```

## 3. Maintenance (File Cleanup)
Set up a cron job to run the cleanup script every 10 minutes:
```bash
*/10 * * * * python /app/scripts/cleanup.py
```

## 4. System Requirements
- **LibreOffice**: Required for Word to PDF conversion.
- **Tesseract (Optional)**: If you want to enable OCR in the future.
- **Redis**: Required if using Celery for background tasks.
