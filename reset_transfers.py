import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from bankapp.models import Account
from django.contrib.auth.models import User

if len(sys.argv) > 1:
    email = sys.argv[1]
    try:
        user = User.objects.get(email=email)
        account = Account.objects.get(user=user)
        account.transfer_count = 0
        account.save()
        print(f"Transfer count reset for user {email}.")
    except User.DoesNotExist:
        print(f"User with email {email} not found.")
    except Account.DoesNotExist:
        print(f"Account for user {email} not found.")
else:
    # Reset transfer_count for all users
    accounts = Account.objects.all()
    for account in accounts:
        account.transfer_count = 0
        account.save()
    print("Transfer counts reset for all users.")