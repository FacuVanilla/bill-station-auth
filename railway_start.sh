#!/bin/bash

# Railway startup script for Django application
# This script handles the PORT environment variable and starts the application

set -e  # Exit on any error

echo "🚀 Starting Django application on Railway..."

# Check if PORT is set
if [ -z "$PORT" ]; then
    echo "⚠️  PORT environment variable not set, using default port 8000"
    export PORT=8000
fi

echo "📍 Using port: $PORT"

# Wait for database to be ready (Railway specific)
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput || {
    echo "❌ Database migration failed"
    exit 1
}

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput || {
    echo "⚠️  Static file collection failed, continuing..."
}

# Create superuser if it doesn't exist (optional)
echo "👤 Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('No superuser found, creating one...')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
" || echo "⚠️  Superuser check failed, continuing..."

# Start the application with Gunicorn
echo "🚀 Starting Gunicorn server on port $PORT..."
exec gunicorn auth_service.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --preload
