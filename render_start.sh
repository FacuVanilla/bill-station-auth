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
# --clear ensures old static files are removed first
python manage.py collectstatic --noinput --clear

# Start Gunicorn with WhiteNoise serving static files
echo "🚀 Starting Gunicorn server..."
exec gunicorn auth_service.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \              # bumped workers (good balance for Render free/Starter)
    --threads 4 \              # improves concurrency for I/O bound requests
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
