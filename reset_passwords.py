import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

"""
Script to reset a specific user's password
Usage: python reset_passwords.py <email> <new_password>
Example: python reset_passwords.py john@bank.com NewPassword123!
"""

if len(sys.argv) < 3:
    print("Usage: python reset_passwords.py <email> <new_password>")
    print("Example: python reset_passwords.py john@bank.com NewPassword123!")
    sys.exit(1)

email = sys.argv[1]
new_password = sys.argv[2]

try:
    user = User.objects.get(email=email)
    user.set_password(new_password)
    user.save()
    print(f"✅ Password reset successfully for {email}")
except User.DoesNotExist:
    print(f"❌ User with email {email} not found")
    sys.exit(1)
