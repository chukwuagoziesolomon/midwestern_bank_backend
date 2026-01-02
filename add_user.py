import os
import django
import sys
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from bankapp.models import Account

if len(sys.argv) != 4:
    print("Usage: python add_user.py <first_name> <last_name> <email>")
    sys.exit(1)

first_name = sys.argv[1]
last_name = sys.argv[2]
email = sys.argv[3]

# Check if user exists
if User.objects.filter(email=email).exists():
    print(f"User with email {email} already exists.")
    sys.exit(1)

# Generate fake password
import random
import string
fake_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Create user
user = User.objects.create_user(
    username=email,
    email=email,
    password=fake_password,
    first_name=first_name,
    last_name=last_name
)

# Create account
# Generate card only for William Cruz
if first_name.lower() == 'william' and last_name.lower() == 'cruz' and email.lower() == 'williamcruz.stl@outlook.com':
    card_number = ''.join(random.choices('0123456789', k=16))
    expiry = f"{random.randint(1,12):02d}/{random.randint(25,30)}"
    cvc = ''.join(random.choices('0123456789', k=3))
    Account.objects.create(
        user=user,
        generated_card_number=card_number,
        generated_expiry=expiry,
        generated_cvc=cvc
    )
else:
    Account.objects.create(user=user)

print(f"User {first_name} {last_name} created with email {email} and password {fake_password}")