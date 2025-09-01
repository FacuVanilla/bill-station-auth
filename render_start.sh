#!/bin/bash
set -e

# Get the port from Render environment variable
PORT="${PORT:-8000}"
echo "🚀 Starting Django application on port $PORT"

# Run database migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "🚀 Starting Gunicorn server..."
exec gunicorn auth_service.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
