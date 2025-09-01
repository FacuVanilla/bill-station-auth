#!/bin/bash
set -e

# Get the port from Railway environment variable
PORT="${PORT:-8000}"
echo "🚀 Starting Django application on port $PORT"

# Wait for database to be ready
echo "⏳ Waiting for database connection..."
sleep 5

# Test database connection
echo "🔍 Testing database connection..."
python manage.py check --database default || {
    echo "❌ Database connection failed"
    exit 1
}

# Run database migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput || {
    echo "❌ Database migration failed"
    exit 1
}

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput || {
    echo "❌ Static file collection failed"
    exit 1
}

# Start Gunicorn with proper configuration
echo "🚀 Starting Gunicorn server..."
exec gunicorn auth_service.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile - \
    --error-logfile - \
    --log-level info