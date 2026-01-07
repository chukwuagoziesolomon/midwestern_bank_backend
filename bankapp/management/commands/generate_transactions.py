import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bankapp.models import Transfer, Account
from decimal import Decimal

class Command(BaseCommand):
    help = 'Generate backdated transaction history from December 2023 to present'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=None,
            help='Specific user ID to generate transactions for, or leave blank for all users'
        )

    def handle(self, *args, **options):
        user_id = options.get('users')
        
        if user_id:
            try:
                users = [User.objects.get(id=user_id)]
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User with ID {user_id} not found'))
                return
        else:
            users = User.objects.all()
        
        if not users:
            self.stdout.write(self.style.WARNING('No users found'))
            return
        
        # Transaction descriptions
        descriptions = [
            'Salary Payment',
            'Freelance Work',
            'Bill Payment',
            'Rent Payment',
            'Online Shopping',
            'Restaurant',
            'Gas Station',
            'Grocery Store',
            'Insurance Premium',
            'Loan Payment',
            'Investment Transfer',
            'Professional Services',
            'Entertainment',
            'Utilities',
            'Medical Expenses'
        ]
        
        # Recipient names
        recipient_names = [
            'John Smith',
            'Sarah Johnson',
            'Michael Brown',
            'Emily Davis',
            'David Wilson',
            'Jessica Miller',
            'Robert Anderson',
            'Jennifer Taylor',
            'James Thomas',
            'Mary Jackson'
        ]
        
        # Banks
        banks = [
            'Chase Bank',
            'Bank of America',
            'Wells Fargo',
            'Citibank',
            'US Bank',
            'PNC Bank',
            'Capital One',
            'TD Bank',
            'Ally Bank',
            'Discover Bank'
        ]
        
        start_date = datetime(2023, 12, 1)
        end_date = datetime(2026, 1, 7)
        total_days = (end_date - start_date).days
        
        transaction_count = 0
        
        for user in users:
            try:
                account = Account.objects.get(user=user)
            except Account.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Account for {user.email} not found'))
                continue
            
            # Generate 15-30 transactions per user
            num_transactions = random.randint(15, 30)
            
            for _ in range(num_transactions):
                # Random date between Dec 2023 and Jan 2026
                random_days = random.randint(0, total_days)
                transaction_date = start_date + timedelta(days=random_days)
                
                # Random time
                transaction_date = transaction_date.replace(
                    hour=random.randint(8, 20),
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59)
                )
                
                # Random amount between 10 and 5000
                amount = Decimal(str(round(random.uniform(10, 5000), 2)))
                
                # Create transfer
                transfer = Transfer.objects.create(
                    user=user,
                    transfer_type=random.choice(['local', 'international']),
                    receiver_name=random.choice(recipient_names),
                    receiver_bank=random.choice(banks),
                    receiver_account_number=f"{random.randint(10000000, 99999999)}",
                    routing_number=f"{random.randint(100000000, 999999999)}",
                    amount=amount,
                    description=random.choice(descriptions),
                    pin='2027',
                    date=transaction_date,
                    status='completed'
                )
                
                transaction_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Generated {num_transactions} transactions for {user.email}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully generated {transaction_count} backdated transactions '
                f'from December 2023 to January 2026!'
            )
        )
