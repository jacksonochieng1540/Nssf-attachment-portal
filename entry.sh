#!/usr/bin/env bash
set -e

# Wait for DB to be available (simple loop)
if [ -n "$DATABASE_HOST" ]; then
  echo "Waiting for database ($DATABASE_HOST:$DATABASE_PORT)..."
  until nc -z -v -w5 "$DATABASE_HOST" "$DATABASE_PORT"; do
    echo "Waiting for database connection..."
    sleep 1
  done
fi

# Apply DB migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create default superuser if needed (optional — disabled by default)
# If you want an automatic superuser in dev, uncomment and set env vars:
# python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL"

exec "$@"
