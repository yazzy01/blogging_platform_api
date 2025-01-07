import os
import sys
from pathlib import Path

# Get the absolute path of the project root directory
root_dir = Path(__file__).resolve().parent
apps_dir = root_dir / 'apps'

# Add the project root and apps directories to Python path
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

if str(apps_dir) not in sys.path:
    sys.path.insert(0, str(apps_dir))

# Print paths for debugging
print(f"Root directory: {root_dir}")
print(f"Apps directory: {apps_dir}")
print(f"Python path: {sys.path}")

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import and create the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
