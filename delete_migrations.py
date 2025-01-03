import os
import glob

# Delete all numbered migration files
migration_path = os.path.join('apps', 'posts', 'migrations')
for file in glob.glob(os.path.join(migration_path, '0*.py')):
    print(f"Deleting {file}")
    os.remove(file)

# Keep __init__.py
print("Done")
