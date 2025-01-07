web: gunicorn --workers=4 --threads=4 core.wsgi:application
worker: celery -A core worker -l info
