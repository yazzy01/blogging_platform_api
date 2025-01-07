web: gunicorn --workers=4 --threads=4 config.wsgi:application
worker: celery -A config worker -l info
