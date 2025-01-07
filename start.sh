#!/bin/bash

# Print debugging information
echo "Current directory: $(pwd)"
echo "Python path before: $PYTHONPATH"
echo "Directory contents:"
ls -la
echo "Apps directory contents:"
ls -la apps/

# Set the Python path
export PYTHONPATH="/app:/app/apps:$PYTHONPATH"
echo "Python path after: $PYTHONPATH"

# Print Python path information
python -c "import sys; print('Python path:', sys.path)"
python -c "import os; print('PYTHONPATH:', os.environ.get('PYTHONPATH'))"

# Run migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Gunicorn with debugging
gunicorn wsgi_handler:application \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --threads 4 \
    --timeout 120 \
    --log-level debug \
    --error-logfile - \
    --access-logfile - \
    --capture-output
