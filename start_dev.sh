#!/bin/bash

# Auth Service Development Startup Script
echo "🚀 Starting Auth Service Development Environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your configuration before continuing"
    echo "Press Enter when ready to continue..."
    read
fi

# Check Django configuration
echo "🔍 Checking Django configuration..."
python manage.py check

if [ $? -eq 0 ]; then
    echo "✅ Django configuration is valid"
    
    # Run migrations if needed
    echo "🔄 Running migrations..."
    python manage.py migrate
    
    echo ""
    echo "🎉 Development environment is ready!"
    echo ""
    echo "Next steps:"
    echo "1. Ensure PostgreSQL and Redis are running"
    echo "2. Start the development server: python manage.py runserver"
    echo "3. Visit http://localhost:8000 for API documentation"
    echo "4. Visit http://localhost:8000/admin for admin interface"
    echo ""
    echo "To start the server now, run: python manage.py runserver"
else
    echo "❌ Django configuration check failed"
    echo "Please fix the issues before continuing"
    exit 1
fi
