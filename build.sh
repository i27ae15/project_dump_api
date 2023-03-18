#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

daphne project_dump.asgi:application -b 0.0.0.0 -p 8000