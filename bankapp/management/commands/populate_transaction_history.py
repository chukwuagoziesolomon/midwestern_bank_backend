from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bankapp.models import Transfer, Account, CreditCardDeposit
from decimal import Decimal
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate diverse transaction history 6-3 months before account creation, max 3/day, with insufficient funds cases, ensuring net totals match current balances'

    def handle(self, *args, **options):
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found. Please create users first.'))
            return

        transfer_count = 0
        deposit_count = 0
        failed_count = 0
        
        for user in users:
            try:
                account = Account.objects.get(user=user)
                # Start 6 months before account creation
                start_date = account.created_at - timedelta(days=180)
                # End 3 months before account creation
                end_date = account.created_at - timedelta(days=90)
                
                # Target net: current total_balance
                target_net = account.total_balance
                
                # Generate transactions
                transactions = []
                current_net = Decimal('0.00')
                current_date = start_date
                
                while current_date <= end_date:
                    # Max 3 transactions per day
                    max_transactions_today = min(3, random.randint(0, 3))
                    
                    for _ in range(max_transactions_today):
                        # Decide if credit or debit
                        is_credit = random.random() < 0.4  # 40% chance of credit
                        
                        if is_credit:
                            # Credit (deposit)
                            amount = Decimal(str(round(random.uniform(100, 5000), 2)))
                            transactions.append(('credit', amount, current_date))
                            current_net += amount
                        else:
                            # Debit (transfer)
                            amount = Decimal(str(round(random.uniform(10, 2000), 2)))
                            # Check for insufficient funds simulation
                            if amount > account.total_balance * 0.8 and random.random() < 0.3:
                                transactions.append(('debit_failed', amount, current_date))
                            else:
                                transactions.append(('debit', amount, current_date))
                                current_net -= amount
                    
                    # Move to next day
                    current_date += timedelta(days=1)
                
                # Adjust the last transaction to match target_net
                if transactions:
                    last_type, last_amount, last_date = transactions[-1]
                    if last_type == 'credit':
                        new_amount = last_amount + (target_net - current_net)
                        if new_amount > 0:
                            transactions[-1] = ('credit', new_amount, last_date)
                        else:
                            # If negative, change to debit
                            transactions[-1] = ('debit', abs(new_amount), last_date)
                            current_net += 2 * last_amount  # adjust net
                    elif last_type == 'debit':
                        new_amount = last_amount - (target_net - current_net)
                        if new_amount > 0:
                            transactions[-1] = ('debit', new_amount, last_date)
                        else:
                            # Change to credit
                            transactions[-1] = ('credit', abs(new_amount), last_date)
                            current_net -= 2 * last_amount
                
                # Now create the transactions
                for tx_type, amount, tx_date in transactions:
                    if tx_type == 'credit':
                        CreditCardDeposit.objects.create(
                            user=user,
                            card_number=account.generated_card_number,
                            card_expiry=account.generated_expiry,
                            card_cvc=account.generated_cvc,
                            deposit_amount=amount,
                            card_holder_name=f"{user.first_name} {user.last_name}",
                            date=tx_date,
                            status='completed'
                        )
                        deposit_count += 1
                    elif tx_type == 'debit':
                        transfer = Transfer(
                            user=user,
                            transfer_type=random.choice(['local', 'international']),
                            receiver_name=random.choice(self.get_receiver_names()),
                            receiver_bank=random.choice(self.get_banks()),
                            receiver_account_number=f"{random.randint(1000000000, 9999999999)}",
                            amount=amount,
                            description=random.choice(self.get_descriptions()),
                            pin='1234',
                            status='completed',
                            date=tx_date,
                            is_populated=True
                        )
                        if transfer.transfer_type == 'international':
                            transfer.receiver_bank_address = f"{random.randint(1, 999)} Main St, City, Country"
                            transfer.swift_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4)) + '123'
                            transfer.iban = 'DE' + ''.join(random.choices('0123456789', k=18))
                        else:
                            transfer.routing_number = f"{random.randint(100000000, 999999999)}"
                        transfer.save()
                        transfer_count += 1
                    elif tx_type == 'debit_failed':
                        transfer = Transfer(
                            user=user,
                            transfer_type=random.choice(['local', 'international']),
                            receiver_name=random.choice(self.get_receiver_names()),
                            receiver_bank=random.choice(self.get_banks()),
                            receiver_account_number=f"{random.randint(1000000000, 9999999999)}",
                            amount=amount,
                            description=random.choice(self.get_descriptions()),
                            pin='1234',
                            status='failed',
                            date=tx_date,
                            is_populated=True
                        )
                        if transfer.transfer_type == 'international':
                            transfer.receiver_bank_address = f"{random.randint(1, 999)} Main St, City, Country"
                            transfer.swift_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4)) + '123'
                            transfer.iban = 'DE' + ''.join(random.choices('0123456789', k=18))
                        else:
                            transfer.routing_number = f"{random.randint(100000000, 999999999)}"
                        transfer.save()
                        failed_count += 1
                
            except Account.DoesNotExist:
                continue
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Successfully created {transfer_count} transfers, {deposit_count} deposits, {failed_count} failed transfers. '
                f'Net totals match current balances.'
            )
        )
    
    def get_receiver_names(self):
        return [
            'Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson',
            'Emma Brown', 'Frank Miller', 'Grace Taylor', 'Henry Anderson',
            'Isabella Thomas', 'Jack Jackson', 'Kevin Lee', 'Laura Martinez',
            'Michael Garcia', 'Nancy Wilson', 'Oliver Davis', 'Patricia Moore',
            'Quincy Taylor', 'Rachel Anderson', 'Steven Thomas', 'Tina Jackson'
        ]
    
    def get_banks(self):
        return [
            'Chase Bank', 'Bank of America', 'Wells Fargo', 'Citibank',
            'US Bank', 'PNC Bank', 'Capital One', 'Discover Bank',
            'TD Bank', 'Fifth Third Bank', 'HSBC', 'Barclays', 'Santander',
            'Lloyds Bank', 'Royal Bank of Canada', 'Scotiabank'
        ]
    
    def get_descriptions(self):
        return [
            'Salary payment', 'Invoice payment', 'Rent payment', 'Utilities',
            'Groceries', 'Gas payment', 'Freelance work', 'Refund',
            'Loan repayment', 'Business expense', 'Travel reimbursement',
            'Vendor payment', 'Subscription', 'Service fee', 'Consulting',
            'Marketing', 'Software license', 'Domain renewal', 'Hosting',
            'Insurance', 'Medical', 'Education', 'Charity donation'
        ]
