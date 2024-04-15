#!/bin/sh

# python manage.py flush --no-input
cd app/
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py runserver 0.0.0.0:8000
exec "$@"