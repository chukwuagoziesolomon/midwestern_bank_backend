import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from bankapp.models import Account, Transfer

# Create William Cruz user if not exists
user, created = User.objects.get_or_create(
    email='williamcruz.stl@outlook.com',
    defaults={
        'username': 'williamcruz.stl@outlook.com',
        'first_name': 'William',
        'last_name': 'Cruz'
    }
)
user.set_password('TempPass123')
user.save()
card_number = ''.join(random.choices('0123456789', k=16))
expiry = f"{random.randint(1,12):02d}/{random.randint(25,30)}"
cvc = ''.join(random.choices('0123456789', k=3))
if created:
    Account.objects.create(
        user=user,
        generated_card_number=card_number,
        generated_expiry=expiry,
        generated_cvc=cvc
    )
else:
    account = Account.objects.get(user=user)
    account.generated_card_number = card_number
    account.generated_expiry = expiry
    account.generated_cvc = cvc
    account.save()

account = Account.objects.get(user=user)

# Create some sample transfers
transfers_data = [
    {
        'transfer_type': 'local',
        'receiver_name': 'John Doe',
        'receiver_bank': 'Local Bank',
        'receiver_account_number': '1234567890',
        'routing_number': '123456789',
        'amount': Decimal('500.00'),
        'description': 'Payment for services',
        'pin': '2027',
        'status': 'completed'
    },
    {
        'transfer_type': 'international',
        'receiver_name': 'Jane Smith',
        'receiver_bank': 'International Bank',
        'receiver_bank_address': '123 Bank St, City, Country',
        'receiver_account_number': '0987654321',
        'iban': 'GB29 NWBK 6016 1331 9268 19',
        'swift_code': 'ABCDUS33',
        'amount': Decimal('1000.00'),
        'description': 'Overseas payment',
        'pin': '2027',
        'status': 'completed'
    },
    {
        'transfer_type': 'local',
        'receiver_name': 'Bob Johnson',
        'receiver_bank': 'Another Bank',
        'receiver_account_number': '1122334455',
        'routing_number': '987654321',
        'amount': Decimal('250.00'),
        'description': 'Refund',
        'pin': '2027',
        'status': 'completed'
    }
]

for data in transfers_data:
    transfer = Transfer.objects.create(user=user, **data)
    # Deduct from balance
    if account.available_balance >= transfer.amount:
        account.available_balance -= transfer.amount
        account.save()

print("Sample transfers populated.")