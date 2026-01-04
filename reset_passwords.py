import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Set password for all users to 'TempPass123'
users = User.objects.all()
for user in users:
    user.set_password('TempPass123')
    user.save()
    print(f"Updated password for {user.email}")

print("All passwords updated to 'TempPass123'")