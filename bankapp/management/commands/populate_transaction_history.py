from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bankapp.models import Transfer, Account
from decimal import Decimal
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate backdated transaction history from December 2023 to January 2026'

    def handle(self, *args, **options):
        # Get the first user (or create sample users if needed)
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found. Please create users first.'))
            return

        start_date = datetime(2023, 12, 1)
        end_date = datetime(2026, 1, 7)
        
        receiver_names = [
            'Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson',
            'Emma Brown', 'Frank Miller', 'Grace Taylor', 'Henry Anderson',
            'Isabella Thomas', 'Jack Jackson'
        ]
        
        receiver_banks = [
            'Chase Bank', 'Bank of America', 'Wells Fargo', 'Citibank',
            'US Bank', 'PNC Bank', 'Capital One', 'Discover Bank',
            'TD Bank', 'Fifth Third Bank'
        ]
        
        descriptions = [
            'Salary payment', 'Invoice payment', 'Rent payment', 'Utilities',
            'Groceries', 'Gas payment', 'Freelance work', 'Refund',
            'Loan repayment', 'Business expense', 'Travel reimbursement',
            'Vendor payment', 'Subscription', 'Service fee'
        ]
        
        transfer_count = 0
        current_date = start_date
        
        while current_date <= end_date:
            # Randomly decide if there's a transaction on this day
            if random.random() > 0.7:  # 30% chance of transaction
                for user in users[:3]:  # Create transactions for first 3 users
                    try:
                        account = Account.objects.get(user=user)
                        
                        # Create transfer
                        transfer = Transfer(
                            user=user,
                            transfer_type=random.choice(['local', 'international']),
                            receiver_name=random.choice(receiver_names),
                            receiver_bank=random.choice(receiver_banks),
                            receiver_account_number=f"{random.randint(1000000000, 9999999999)}",
                            amount=Decimal(str(round(random.uniform(50, 5000), 2))),
                            description=random.choice(descriptions),
                            pin='1234',
                            status='completed',
                            date=current_date
                        )
                        
                        # For international transfers, add extra fields
                        if transfer.transfer_type == 'international':
                            transfer.receiver_bank_address = f"{random.randint(1, 999)} Main St, City, Country"
                            transfer.swift_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4)) + '123'
                            transfer.iban = 'DE' + ''.join(random.choices('0123456789', k=18))
                        else:
                            transfer.routing_number = f"{random.randint(100000000, 999999999)}"
                        
                        transfer.save()
                        transfer_count += 1
                        
                    except Account.DoesNotExist:
                        continue
            
            # Move to next day
            current_date += timedelta(days=1)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully created {transfer_count} backdated transactions '
                f'from {start_date.strftime("%B %d, %Y")} to {end_date.strftime("%B %d, %Y")}'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Transaction history now spans approximately 13 months of data!'
            )
        )
