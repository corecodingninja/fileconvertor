from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery
import os

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
celery = Celery()


def create_app(config_name=None):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Load config
    from app.config import config
    cfg = config.get(config_name or os.getenv('FLASK_ENV', 'development'))
    app.config.from_object(cfg)

    # Init extensions
    db.init_app(app)
    limiter.init_app(app)

    # Init Celery
    celery.conf.update(
        broker_url=app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
        result_backend=app.config.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.converter import converter_bp
    from app.routes.blog import blog_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(converter_bp)
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(api_bp, url_prefix='/api')

    # SEO Context Processor
    from app.utils.seo import get_json_ld
    @app.context_processor
    def inject_seo():
        return dict(get_json_ld=get_json_ld)

    # Error Handlers
    from flask import jsonify
    from flask_limiter.errors import RateLimitExceeded
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(e):
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

    # Create DB tables
    with app.app_context():
        db.create_all()

    return app
