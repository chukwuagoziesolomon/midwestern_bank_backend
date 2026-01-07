#!/bin/bash
# Build script for Render deployment - PLACE THIS IN REPO ROOT
# This script runs during deployment to set up the application

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
echo "   ADMIN_EMAIL: ${ADMIN_EMAIL:-admin@midwesternbank.com}"

if python manage.py create_superuser_auto; then
  echo "✅ Admin account setup successful"
else
  echo "⚠️  create_superuser_auto failed, attempting fallback..."
  python manage.py shell << EOF
from django.contrib.auth.models import User
from bankapp.models import Account
import os
import random

email = os.getenv('ADMIN_EMAIL', 'admin@midwesternbank.com')
password = os.getenv('ADMIN_PASSWORD', 'AdminPassword123!')

try:
    # Delete if exists
    User.objects.filter(email=email).delete()
    
    # Create superuser
    admin = User.objects.create_superuser(email, email, password, 'Admin', 'User')
    print(f'✅ User created: {email}')
    
    # Create account
    card = ''.join(random.choices('0123456789', k=16))
    expiry = f'{random.randint(1,12):02d}/{random.randint(25,30)}'
    cvc = ''.join(random.choices('0123456789', k=3))
    
    Account.objects.create(
        user=admin,
        generated_card_number=card,
        generated_expiry=expiry,
        generated_cvc=cvc,
        is_approved=True
    )
    print(f'✅ Account created and approved')
    print(f'✅ Admin ready: {email} / {password}')
except Exception as e:
    print(f'❌ Error: {str(e)}')
    exit(1)
EOF
fi

echo "✅ Deployment setup complete!"
