# Email Configuration - Quick Start

## Step 1: Create `.env` file in your project root

Create a file named `.env` in the same directory as `manage.py`:

```env
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=noreply@midwesternbank.com
```

## Step 2: Install python-dotenv (if not already installed)

```bash
pip install python-dotenv
```

## Step 3: Load environment variables in settings.py

The settings.py already includes support for environment variables using `os.getenv()`.

## Step 4: Get Gmail App Password

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable 2-Factor Authentication (if not already enabled)
3. Search for "App passwords" in security settings
4. Generate an app password for "Mail" and "Windows Computer"
5. Copy the 16-character password (no spaces)
6. Paste it as `EMAIL_HOST_PASSWORD` in `.env`

## Step 5: Test Email Sending

### Option A: Console Backend (Development)

Update `.env`:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

This prints emails to console instead of sending them.

### Option B: Test with Real Email

1. Use SMTP configuration from Step 1
2. Make a transaction in your application
3. Both sender and receiver will receive emails

## Quick Test Script

Create a file `test_email.py` in your project root:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from bankapp.models import Account, Transfer
from bankapp.services import TransactionEmailService
from decimal import Decimal

# Create test user
user = User.objects.first()
account = Account.objects.filter(user=user).first()

if user and account:
    # Create a test transfer
    transfer = Transfer.objects.create(
        user=user,
        transfer_type='local',
        receiver_name='Test Receiver',
        receiver_bank='Test Bank',
        receiver_account_number='1234567890',
        amount=Decimal('100.00'),
        description='Test transfer',
        pin='1234'
    )
    
    # Send emails
    print("Sending debit alert...")
    debit_result = TransactionEmailService.send_debit_alert(user, account, transfer)
    print(f"Debit alert: {'Sent' if debit_result else 'Failed'}")
    
    print("\nSending credit alert...")
    credit_result = TransactionEmailService.send_credit_alert(
        'receiver@example.com',
        transfer.receiver_name,
        user,
        account,
        transfer
    )
    print(f"Credit alert: {'Sent' if credit_result else 'Failed'}")
else:
    print("No user found in database")
```

Run it:
```bash
python test_email.py
```

## Troubleshooting

### "Connection refused" or "Network error"

- Check EMAIL_HOST and EMAIL_PORT are correct
- Check internet connection
- Try using console backend for testing

### "Authentication failed"

- Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct
- Use App Password, not your regular Gmail password
- Make sure 2FA is enabled on Gmail account

### "Module not found: dotenv"

- Install python-dotenv: `pip install python-dotenv`

### Emails not sending

- Check EMAIL_BACKEND setting
- Look at Django logs for errors
- Try console backend to see email content
- Verify environment variables are loaded

## Production Deployment

For production, use environment variables in your hosting platform:

**Render.com:**
1. Go to Dashboard → Your Service → Environment
2. Add variables:
   - `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
   - `EMAIL_HOST=smtp.gmail.com`
   - `EMAIL_PORT=587`
   - `EMAIL_USE_TLS=True`
   - `EMAIL_HOST_USER=your-email@gmail.com`
   - `EMAIL_HOST_PASSWORD=your-app-password`
   - `DEFAULT_FROM_EMAIL=noreply@midwesternbank.com`

**Heroku:**
```bash
heroku config:set EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
heroku config:set EMAIL_HOST=smtp.gmail.com
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_USE_TLS=True
heroku config:set EMAIL_HOST_USER=your-email@gmail.com
heroku config:set EMAIL_HOST_PASSWORD=your-app-password
heroku config:set DEFAULT_FROM_EMAIL=noreply@midwesternbank.com
```

## Next Steps

1. Read [EMAIL_INTEGRATION_GUIDE.md](EMAIL_INTEGRATION_GUIDE.md) for full documentation
2. Customize email templates in `/bankapp/templates/emails/`
3. Update bank info in `TransactionEmailService` class
4. Test email sending with test script
5. Deploy to production with environment variables

Enjoy your beautiful email notifications! 🎉
