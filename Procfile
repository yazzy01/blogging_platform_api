web: gunicorn blogging_platform_api.wsgi:application
worker: celery -A blogging_platform_api worker -l info
