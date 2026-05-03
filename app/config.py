import os
from datetime import timedelta


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-in-prod')
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp/fileconverter')
    FILE_RETENTION_MINUTES = 10
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    RATELIMIT_DEFAULT = '200 per day;50 per hour'
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    ALLOWED_WORD_EXTENSIONS = {'.docx', '.doc'}
    ALLOWED_PDF_EXTENSIONS = {'.pdf'}
    ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
    ALLOWED_WORD_MIMES = {
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/msword',
    }
    ALLOWED_PDF_MIMES = {'application/pdf'}
    ALLOWED_IMAGE_MIMES = {'image/png', 'image/jpeg', 'image/webp', 'image/bmp'}
    MAX_CONCURRENT_JOBS_PER_IP = 2
    RATE_LIMIT_PER_HOUR = 10
    SITE_URL = os.getenv('SITE_URL', 'http://localhost:5001')
    SITE_NAME = 'ConverterHub'
    SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'corecodingninja@gmail.com')
    GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID', 'G-6NNFF8M7FY')
    ADSENSE_CLIENT = os.getenv('ADSENSE_CLIENT', 'ca-pub-5635730488302512')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    # Use DATABASE_URL from env, fallback to sqlite but warn (Render/Heroku provide this)
    db_url = os.getenv('DATABASE_URL')
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = db_url or 'sqlite:///prod.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
