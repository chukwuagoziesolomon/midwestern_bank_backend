# Email Notification System - Implementation Guide

## Overview

A beautiful, professional HTML email notification system has been integrated into your banking application. When users make transactions, both the sender and receiver receive elegantly designed email alerts.

## Features

✅ **Beautiful HTML Templates**
- Professional, responsive design
- Works on all email clients (Gmail, Outlook, Apple Mail, etc.)
- Mobile-optimized
- Consistent branding

✅ **Two Alert Types**
1. **Debit Alert** (Red theme) - Sent to transaction sender
2. **Credit Alert** (Green theme) - Sent to transaction receiver

✅ **Rich Information**
- Transaction amount and type
- Recipient/Sender details
- Transaction ID and timestamp
- Updated account balances
- Security notices
- Links to dashboard and support

---

## 📁 Files Created

### 1. **Email Templates**

#### `/bankapp/templates/emails/transaction_debit.html`
- Beautiful debit alert template (red theme)
- Shows money leaving the account
- Displays recipient details
- Responsive design

#### `/bankapp/templates/emails/transaction_credit.html`
- Beautiful credit alert template (green theme)
- Shows money received
- Displays sender details
- Responsive design

### 2. **Email Service Module**

#### `/bankapp/services.py`
Complete email service class with:
- `TransactionEmailService` class
- `send_debit_alert()` - Sends alert to transaction sender
- `send_credit_alert()` - Sends alert to transaction receiver
- `get_email_context()` - Generates template context
- Plain text fallback for non-HTML clients

### 3. **Modified Files**

#### `/bankapp/views.py`
- Integrated email sending into `TransferView.post()`
- Sends debit alert automatically on successful transfer
- Sends credit alert to receiver (if email provided)

#### `/config/settings.py`
- Added email configuration settings
- Supports multiple email backends
- Environment variable support for credentials

---

## 🔧 Configuration

### Email Backend Setup

The system supports multiple email backends. Choose one:

#### **Option 1: Console Backend (Development)**
```python
# .env or environment variable
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
Emails will be printed to console instead of being sent. Perfect for testing!

#### **Option 2: SMTP Gmail**
```python
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password  # Use App Password, not regular password
DEFAULT_FROM_EMAIL=noreply@midwesternbank.com
```

#### **Option 3: SendGrid**
```python
EMAIL_BACKEND=sendgrid_backend.SendgridBackend
SENDGRID_API_KEY=your-sendgrid-api-key
```

#### **Option 4: AWS SES**
```python
EMAIL_BACKEND=django_ses.SESBackend
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_SES_REGION_NAME=us-east-1
AWS_SES_REGION_ENDPOINT=email.us-east-1.amazonaws.com
```

---

## 📧 How to Get Gmail App Password

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Factor Authentication
3. Generate an "App Password" for Gmail
4. Use this 16-character password in `EMAIL_HOST_PASSWORD`

**Important:** Never use your actual Gmail password!

---

## 📝 Usage in Code

### Automatic Email Sending

Emails are automatically sent when a transfer is completed:

```python
# In TransferView.post()
transfer.status = 'completed'
transfer.save()

# Debit alert sent to sender automatically
TransactionEmailService.send_debit_alert(user, account, transfer)

# Credit alert sent to receiver (if email provided)
if receiver_email:
    TransactionEmailService.send_credit_alert(
        receiver_email,
        transfer.receiver_name,
        user,
        account,
        transfer
    )
```

### Manual Email Sending

You can also send emails manually:

```python
from bankapp.services import TransactionEmailService

# Send debit alert
TransactionEmailService.send_debit_alert(user, account, transfer)

# Send credit alert
TransactionEmailService.send_credit_alert(
    receiver_email='receiver@example.com',
    receiver_name='John Doe',
    user=sender_user,
    account=sender_account,
    transfer=transfer_object
)
```

---

## 🎨 Customization

### Modify Template Variables

In `services.py`, update the `TransactionEmailService` class constants:

```python
class TransactionEmailService:
    BANK_NAME = "Midwestern Bank"           # Change to your bank name
    SUPPORT_EMAIL = "support@bank.com"      # Your support email
    SUPPORT_PHONE = "+1 (800) 123-4567"     # Your support phone
    CURRENCY = "$"                           # Currency symbol
```

### Update Links

In the `get_email_context()` method, update the URLs:

```python
'dashboard_url': 'https://yourbank.com/dashboard',
'support_url': 'https://yourbank.com/support',
'settings_url': 'https://yourbank.com/settings',
'help_url': 'https://yourbank.com/help',
```

### Modify HTML Templates

Edit the template files directly:
- `/bankapp/templates/emails/transaction_debit.html`
- `/bankapp/templates/emails/transaction_credit.html`

Templates use Django template syntax with `{{ variable }}` placeholders.

---

## 📊 Template Variables Reference

Both templates receive these variables:

```python
{
    'user_name': 'John Doe',                           # Recipient name
    'amount': '1,234.56',                              # Formatted amount
    'currency': '$',                                   # Currency symbol
    'available_balance': '8,765.43',                   # Available balance
    'total_balance': '9,000.00',                       # Total balance
    'transfer_type': 'Local',                          # local/international
    'description': 'Payment for invoice',              # Transaction description
    'transaction_date': 'January 06, 2025 at 03:45 PM', # Formatted timestamp
    'transaction_id': 'TXN-000123-20250106',          # Unique transaction ID
    'bank_name': 'Midwestern Bank',                    # Bank name
    'support_email': 'support@midwesternbank.com',    # Support email
    'support_phone': '+1 (800) 123-4567',             # Support phone
    'current_year': 2025,                              # Current year
    'dashboard_url': 'https://yourbank.com/dashboard',
    'support_url': 'https://yourbank.com/support',
    'settings_url': 'https://yourbank.com/settings',
    'help_url': 'https://yourbank.com/help',
    
    # Debit alert specific
    'receiver_name': 'Jane Smith',                     # Recipient name
    'receiver_bank': 'Bank XYZ',                       # Recipient bank
    'receiver_account_number': '****1234',            # Recipient account
    
    # Credit alert specific
    'sender_name': 'John Doe',                         # Sender name
    'sender_bank': 'Your Account',                     # Sender bank info
}
```

---

## 🧪 Testing

### Test with Console Backend

1. Set in your environment or `.env`:
   ```
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```

2. Make a transfer via API
3. Check your console/logs - emails will be printed there

### Test with Real Email

1. Configure SMTP settings in `.env`:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

2. Make a transfer via API
3. Check your inbox!

---

## 📋 API Integration

### Transfer Endpoint

When creating a transfer, include the receiver's email:

```json
POST /api/transfer/
{
    "user_id": 1,
    "receiver_email": "receiver@example.com",
    "receiver_name": "Jane Smith",
    "receiver_bank": "Bank XYZ",
    "receiver_account_number": "1234567890",
    "transfer_type": "local",
    "amount": "100.00",
    "description": "Payment for services"
}
```

---

## 🚀 Best Practices

1. **Always Use App Passwords**: Never use your actual password
2. **Test First**: Use console backend for testing
3. **Monitor Sending**: Check email logs regularly
4. **Handle Failures**: The service returns `True/False` for success/failure
5. **Security**: Store credentials in environment variables, never in code
6. **Customization**: Update bank name, support info, and URLs for your brand

---

## ⚙️ Environment Variables Template

Create a `.env` file:

```
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=noreply@midwesternbank.com

# Other settings
DEBUG=True
SECRET_KEY=your-secret-key
```

---

## 🐛 Troubleshooting

### Emails not sending?

1. **Check EMAIL_BACKEND**: Is it correctly configured?
2. **Check credentials**: Are EMAIL_HOST_USER and EMAIL_HOST_PASSWORD correct?
3. **Console backend**: Enable console backend to see what's happening
4. **Check logs**: Look for error messages in Django logs
5. **Test manually**: 
   ```python
   from django.core.mail import send_mail
   send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
   ```

### Templates not found?

1. Check that templates directory exists: `/bankapp/templates/emails/`
2. Verify `TEMPLATES['DIRS']` includes template directory in settings
3. Restart Django server after adding templates

### Variables not rendering?

1. Check template syntax: `{{ variable_name }}`
2. Verify context keys match template variable names
3. Check for typos in variable names

---

## 📞 Support

For issues or customizations, refer to:
- [Django Email Documentation](https://docs.djangoproject.com/en/6.0/topics/email/)
- [Django Templates](https://docs.djangoproject.com/en/6.0/topics/templates/)
- [Email Client CSS Support](https://www.campaignmonitor.com/css/)

---

**Happy emailing! 🎉**
