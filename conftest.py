import os
import sys
from pathlib import Path

# Get the absolute path of the project root directory
root_dir = Path(__file__).resolve().parent

# Add the project root and apps directories to Python path
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / 'apps'))
