from app import create_app, celery

app = create_app()

if __name__ == '__main__':
    # Usage:
    # Flask: python run.py
    # Celery: celery -A run.celery worker --loglevel=info
    
    # Using port 5001 because port 5000 is often occupied by macOS AirPlay Receiver
    app.run(debug=True, host='0.0.0.0', port=5001)
