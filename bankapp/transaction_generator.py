"""
Service to generate dummy transaction history for approved users.
Creates backdated transactions from December 2023 to present.
"""

from django.contrib.auth.models import User
from .models import Transfer, Account
from decimal import Decimal
from datetime import datetime, timedelta
import random

class DummyTransactionGenerator:
    """Generate realistic dummy transaction history for users"""
    
    # Common receiver names
    RECEIVER_NAMES = [
        "Sarah Johnson", "Michael Chen", "Emma Davis", "James Wilson",
        "Lisa Anderson", "David Martinez", "Jennifer Taylor", "Robert Brown",
        "Maria Garcia", "Christopher Lee", "Amanda White", "Daniel Harris",
        "Nicole Martin", "Kevin Thompson", "Rachel Moore", "Brandon Jackson"
    ]
    
    # Common banks
    BANKS = [
        "Chase Bank", "Bank of America", "Wells Fargo", "Citibank",
        "TD Bank", "Capital One", "US Bank", "PNC Bank",
        "Navy Federal Credit Union", "USAA Bank", "State Street Bank", "HSBC"
    ]
    
    # Common transaction descriptions
    DESCRIPTIONS = [
        "Salary Payment", "Rent Payment", "Freelance Work", "Consulting Fee",
        "Invoice Payment", "Loan Repayment", "Transfer to Savings", "Payment for Services",
        "Dividend Payment", "Bonus Payment", "Refund", "Reimbursement",
        "Utility Payment", "Insurance Premium", "Medical Expense", "Educational Fee"
    ]
    
    @staticmethod
    def generate_transactions_for_user(user, num_transactions=15, start_date=None, end_date=None):
        """
        Generate dummy transactions for a user within a date range
        
        Args:
            user: User object
            num_transactions: Number of transactions to create (default 15)
            start_date: Start date as datetime object or string (YYYY-MM-DD). Default: Dec 1, 2023
            end_date: End date as datetime object or string (YYYY-MM-DD). Default: Today
        """
        try:
            account = Account.objects.get(user=user)
            
            # Parse dates if provided as strings
            if start_date is None:
                start_date = datetime(2023, 12, 1)
            elif isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            
            if end_date is None:
                end_date = datetime.now()
            elif isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Ensure end_date is at end of day
            end_date = end_date.replace(hour=23, minute=59, second=59)
            
            # Generate transactions
            for i in range(num_transactions):
                # Random date between start and end
                random_days = random.randint(0, (end_date - start_date).days)
                transaction_date = start_date + timedelta(days=random_days)
                
                # Random time of day
                transaction_date = transaction_date.replace(
                    hour=random.randint(8, 17),
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59)
                )
                
                # Random amount between $100 and $5000
                amount = Decimal(str(random.randint(100, 5000)))
                
                # Create transfer
                Transfer.objects.create(
                    user=user,
                    transfer_type=random.choice(['local', 'international']),
                    receiver_name=random.choice(DummyTransactionGenerator.RECEIVER_NAMES),
                    receiver_bank=random.choice(DummyTransactionGenerator.BANKS),
                    receiver_account_number=''.join(random.choices('0123456789', k=10)),
                    routing_number=''.join(random.choices('0123456789', k=9)),
                    amount=amount,
                    description=random.choice(DummyTransactionGenerator.DESCRIPTIONS),
                    pin='1234',  # Dummy PIN
                    date=transaction_date,
                    status='completed',
                    is_populated=True
                )
            
            return True
        
        except Account.DoesNotExist:
            print(f"Account not found for user {user.email}")
            return False
        except Exception as e:
            print(f"Error generating transactions: {str(e)}")
            return False
    
    @staticmethod
    def generate_deposit_history_for_user(user, num_deposits=5, start_date=None, end_date=None):
        """
        Generate dummy credit card deposits for a user within a date range
        
        Args:
            user: User object
            num_deposits: Number of deposits to create (default 5)
            start_date: Start date as datetime object or string (YYYY-MM-DD). Default: Dec 1, 2023
            end_date: End date as datetime object or string (YYYY-MM-DD). Default: Today
        """
        try:
            from .models import CreditCardDeposit
            from .models import Account
            
            account = Account.objects.get(user=user)
            
            # Parse dates if provided as strings
            if start_date is None:
                start_date = datetime(2023, 12, 1)
            elif isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            
            if end_date is None:
                end_date = datetime.now()
            elif isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Ensure end_date is at end of day
            end_date = end_date.replace(hour=23, minute=59, second=59)
            
            for i in range(num_deposits):
                random_days = random.randint(0, (end_date - start_date).days)
                deposit_date = start_date + timedelta(days=random_days)
                deposit_date = deposit_date.replace(
                    hour=random.randint(8, 17),
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59)
                )
                
                deposit_amount = Decimal(str(random.randint(500, 3000)))
                
                CreditCardDeposit.objects.create(
                    user=user,
                    card_number=account.generated_card_number,
                    card_expiry=account.generated_expiry,
                    card_cvc=account.generated_cvc,
                    deposit_amount=deposit_amount,
                    card_holder_name=f"{user.first_name} {user.last_name}",
                    date=deposit_date,
                    status='completed'
                )
            
            return True
        
        except Exception as e:
            print(f"Error generating deposit history: {str(e)}")
            return False
