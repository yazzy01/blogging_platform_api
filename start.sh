#!/bin/bash

# Print debugging information
echo "Current directory: $(pwd)"
echo "Python path before: $PYTHONPATH"

# Set the Python path
export PYTHONPATH="/app:/app/apps:$PYTHONPATH"

echo "Python path after: $PYTHONPATH"
echo "Directory contents:"
ls -la

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Gunicorn with debugging
gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --threads 4 \
    --timeout 120 \
    --log-level debug \
    --error-logfile - \
    --access-logfile - \
    --capture-output
