import os
from pathlib import Path

# Get the absolute path of the project root directory
root_dir = Path(__file__).resolve().parent

# Print paths for debugging
print(f"Root directory: {root_dir}")

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import and create the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
