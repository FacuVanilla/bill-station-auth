#!/bin/bash

# Railway startup script for Django application
# This script handles the PORT environment variable and starts the application

echo "🚀 Starting Django application on Railway..."

# Check if PORT is set
if [ -z "$PORT" ]; then
    echo "⚠️  PORT environment variable not set, using default port 8000"
    export PORT=8000
fi

echo "📍 Using port: $PORT"

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start the application with Gunicorn
echo "🚀 Starting Gunicorn server on port $PORT..."
exec gunicorn auth_service.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
