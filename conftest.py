import os
import sys
from pathlib import Path

# Get the absolute path of the project root directory
root_dir = Path(__file__).resolve().parent

# Add the project root and apps directories to Python path
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

apps_dir = root_dir / 'apps'
if str(apps_dir) not in sys.path:
    sys.path.insert(0, str(apps_dir))

# Also set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = f"{str(root_dir)}:{str(apps_dir)}:{os.environ.get('PYTHONPATH', '')}"
