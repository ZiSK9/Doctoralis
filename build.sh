#!/usr/bin/env bash
# Render build script — exit on error
set -o errexit

pip install -r requirements.txt

# Collect static files (served by WhiteNoise)
python manage.py collectstatic --no-input

# Apply migrations (idempotent; keeps the committed demo DB in sync)
python manage.py migrate
