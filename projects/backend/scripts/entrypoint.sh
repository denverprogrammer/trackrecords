#!/bin/sh

pip list

set -e

ls -lac

python manage.py wait_for_db
sleep 10

if [ "$DEBUG" = 1 ]
then
    python manage.py makemigrations
    python manage.py migrate --no-input

    python manage.py loaddata admin_interface_theme_django.json
    python manage.py loaddata admin_interface_theme_bootstrap.json
    python manage.py loaddata admin_interface_theme_foundation.json
    python manage.py loaddata admin_interface_theme_uswds.json
fi

python manage.py collectstatic --no-input --clear

gunicorn configuration.asgi:application \
    -w 2 \
    -k uvicorn.workers.UvicornWorker \
    --name gunicorn_worker \
    --workers 3 \
    --timeout 120 \
    --log-level debug \
    --bind 0.0.0.0:8000 \
    --reload

exec "$@"
