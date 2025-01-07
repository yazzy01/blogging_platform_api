web: gunicorn core.wsgi:application
worker: celery -A blogging_platform_api worker -l info
