#!/bin/sh
set -e

echo "==> [1/4] Collecte des fichiers statiques (collectstatic)"
python manage.py collectstatic --noinput

echo "==> [2/4] Upload des assets vers Azure Blob Storage"
python jobs/initialize_azure.py

echo "==> [3/4] Application des migrations"
python manage.py migrate --noinput

echo "==> [4/4] Démarrage de Gunicorn"
exec gunicorn job_board.wsgi:application --bind 0.0.0.0:8000 --workers 2
