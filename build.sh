#!/bin/bash
# Build script for Render deployment - PLACE THIS IN REPO ROOT
# This script runs during deployment to set up the application

set -o errexit

echo "🚀 Starting Midwestern Bank deployment..."

# Install Python dependencies
echo "📦 Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Collect static files (optional for API, skip if it fails)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear 2>/dev/null || echo "⚠️  Static files collection skipped"

# Create superuser if it doesn't exist
echo "👤 Setting up admin account..."
python manage.py create_superuser_auto

echo "✅ Deployment setup complete!"
