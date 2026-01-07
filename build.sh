#!/bin/bash
# Build script for Render deployment
# This script runs during deployment to set up the application

set -o errexit

echo "🚀 Starting Midwestern Bank deployment..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "👤 Setting up admin account..."
python manage.py create_superuser_auto

echo "✅ Deployment setup complete!"
