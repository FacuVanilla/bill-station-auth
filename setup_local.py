#!/usr/bin/env python3
"""
Local development setup script for Auth Service
This script helps set up the local development environment
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        return False
    
    # Check if PostgreSQL is running
    try:
        result = subprocess.run("pg_isready", shell=True, capture_output=True)
        if result.returncode != 0:
            print("⚠️  PostgreSQL is not running. Please start PostgreSQL service.")
            return False
    except FileNotFoundError:
        print("⚠️  PostgreSQL client not found. Please install PostgreSQL.")
        return False
    
    # Check if Redis is running
    try:
        result = subprocess.run("redis-cli ping", shell=True, capture_output=True)
        if result.returncode != 0:
            print("⚠️  Redis is not running. Please start Redis service.")
            return False
    except FileNotFoundError:
        print("⚠️  Redis client not found. Please install Redis.")
        return False
    
    print("✅ All dependencies are available")
    return True

def setup_environment():
    """Set up environment variables"""
    print("🔧 Setting up environment...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        try:
            with open("env.example", "r") as template:
                with open(".env", "w") as env:
                    env.write(template.read())
            print("✅ .env file created successfully")
        except FileNotFoundError:
            print("❌ env.example file not found")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def setup_database():
    """Set up the database"""
    print("🗄️  Setting up database...")
    
    # Create database if it doesn't exist
    db_name = "auth_service_db"
    try:
        result = subprocess.run(f"createdb {db_name}", shell=True, capture_output=True)
        if result.returncode == 0:
            print(f"✅ Database '{db_name}' created successfully")
        else:
            print(f"ℹ️  Database '{db_name}' might already exist")
    except FileNotFoundError:
        print("❌ createdb command not found. Please install PostgreSQL client tools.")
        return False
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    return True

def run_migrations():
    """Run database migrations"""
    print("🔄 Running database migrations...")
    
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return False
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        return False
    
    return True

def create_superuser():
    """Create a superuser account"""
    print("👤 Creating superuser account...")
    
    # Check if superuser already exists
    try:
        result = subprocess.run(
            "python manage.py shell -c \"from users.models import User; print('Superuser exists' if User.objects.filter(is_superuser=True).exists() else 'No superuser')\"",
            shell=True, capture_output=True, text=True
        )
        
        if "Superuser exists" in result.stdout:
            print("✅ Superuser already exists")
            return True
    except:
        pass
    
    # Create superuser interactively
    print("📝 Please create a superuser account:")
    if not run_command("python manage.py createsuperuser", "Creating superuser"):
        print("⚠️  Superuser creation failed. You can create one later with: python manage.py createsuperuser")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Auth Service Local Development Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Run setup steps
    steps = [
        ("Checking dependencies", check_dependencies),
        ("Setting up environment", setup_environment),
        ("Setting up database", setup_database),
        ("Installing dependencies", install_dependencies),
        ("Running migrations", run_migrations),
        ("Creating superuser", create_superuser),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please fix the issue and run the script again.")
            sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the development server: python manage.py runserver")
    print("2. Visit http://localhost:8000 to see the API documentation")
    print("3. Visit http://localhost:8000/admin to access the admin interface")
    print("\nHappy coding! 🚀")

if __name__ == "__main__":
    main()
