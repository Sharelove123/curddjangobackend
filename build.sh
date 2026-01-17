#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Starting build process ==="

pip install -r requirements.txt

echo "=== Running collectstatic ==="
python manage.py collectstatic --no-input

echo "=== Running migrations ==="
python manage.py migrate --run-syncdb

echo "=== Build complete ==="
