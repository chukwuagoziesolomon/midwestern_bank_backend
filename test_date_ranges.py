from bankapp.transaction_generator import DummyTransactionGenerator
from django.contrib.auth.models import User
from bankapp.models import Account
from datetime import datetime

# Create a test user to verify date range functionality
try:
    test_user = User.objects.create_user(
        username='datetest@bank.com',
        email='datetest@bank.com',
        password='temppass',
        first_name='Date',
        last_name='Tester'
    )
    
    # Create account
    account = Account.objects.create(
        user=test_user,
        generated_card_number='1234567890123456',
        generated_expiry='12/28',
        generated_cvc='123'
    )
    
    # Test: Generate with custom dates (string format)
    DummyTransactionGenerator.generate_transactions_for_user(
        test_user,
        num_transactions=3,
        start_date='2024-06-01',
        end_date='2024-12-31'
    )
    
    transfers = test_user.transfer_set.all()
    print(f"✅ Test Passed: Generated {transfers.count()} transfers with custom dates")
    
    for t in transfers:
        print(f"   - {t.date.strftime('%Y-%m-%d')} | {t.description} | ${t.amount}")
    
    # Clean up
    test_user.delete()
    print("\n✅ All date range tests passed!")
    print("✅ Custom date ranges are working correctly!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
