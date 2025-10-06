#!/usr/bin/env bash
set -e

if [ -n "$DATABASE_HOST" ]; then
  echo "Waiting for database ($DATABASE_HOST:$DATABASE_PORT)..."
  until nc -z -v -w5 "$DATABASE_HOST" "$DATABASE_PORT"; do
    echo "Waiting for database connection..."
    sleep 1
  done
fi


echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput



exec "$@"
