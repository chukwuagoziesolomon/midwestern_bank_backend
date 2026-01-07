from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime


class TransactionEmailService:
    """
    Service class to handle sending transaction notification emails.
    Supports both debit (sender) and credit (receiver) alerts.
    """
    
    BANK_NAME = "Midwestern Bank"
    SUPPORT_EMAIL = "support@midwesternbank.com"
    SUPPORT_PHONE = "+1 (800) 123-4567"
    CURRENCY = "$"
    
    @staticmethod
    def get_email_context(user, account, transfer, email_type='debit'):
        """
        Generate context data for email templates.
        
        Args:
            user: Django User object
            account: Account object
            transfer: Transfer object
            email_type: 'debit' or 'credit'
        
        Returns:
            Dictionary with template context
        """
        user_full_name = f"{user.first_name} {user.last_name}".strip()
        if not user_full_name:
            user_full_name = user.email
        
        # Format currency
        amount_formatted = f"{float(transfer.amount):,.2f}"
        balance_formatted = f"{float(account.available_balance):,.2f}"
        total_balance_formatted = f"{float(account.total_balance):,.2f}"
        
        # Format date
        transaction_date = transfer.date.strftime("%B %d, %Y at %I:%M %p")
        current_year = datetime.now().year
        
        context = {
            'user_name': user_full_name,
            'amount': amount_formatted,
            'currency': TransactionEmailService.CURRENCY,
            'available_balance': balance_formatted,
            'total_balance': total_balance_formatted,
            'transfer_type': transfer.transfer_type.capitalize(),
            'description': transfer.description,
            'transaction_date': transaction_date,
            'transaction_id': f"TXN-{transfer.id:06d}-{transfer.date.strftime('%Y%m%d')}",
            'bank_name': TransactionEmailService.BANK_NAME,
            'support_email': TransactionEmailService.SUPPORT_EMAIL,
            'support_phone': TransactionEmailService.SUPPORT_PHONE,
            'current_year': current_year,
            # URLs - adjust these based on your frontend URLs
            'dashboard_url': 'https://yourbank.com/dashboard',
            'support_url': 'https://yourbank.com/support',
            'settings_url': 'https://yourbank.com/settings',
            'help_url': 'https://yourbank.com/help',
        }
        
        if email_type == 'debit':
            context.update({
                'receiver_name': transfer.receiver_name,
                'receiver_bank': transfer.receiver_bank,
                'receiver_account_number': transfer.receiver_account_number,
            })
        elif email_type == 'credit':
            # For credit alert, we need the sender's name
            context.update({
                'sender_name': user_full_name,
                'sender_bank': "Your Account",
            })
        
        return context
    
    @staticmethod
    def send_debit_alert(user, account, transfer):
        """
        Send debit alert email to the sender (user who initiated the transfer).
        
        Args:
            user: Django User object (sender)
            account: Account object
            transfer: Transfer object
        
        Returns:
            Boolean indicating success
        """
        try:
            context = TransactionEmailService.get_email_context(
                user, account, transfer, email_type='debit'
            )
            
            # Render HTML template
            html_message = render_to_string(
                'emails/transaction_debit.html',
                context
            )
            
            # Create email
            subject = f"Debit Alert: {TransactionEmailService.CURRENCY}{context['amount']} transferred"
            email = EmailMultiAlternatives(
                subject=subject,
                body=TransactionEmailService._get_plain_text_version(context, 'debit'),
                from_email=f"noreply@{TransactionEmailService.BANK_NAME.lower().replace(' ', '')}.com",
                to=[user.email]
            )
            
            # Attach HTML version
            email.attach_alternative(html_message, "text/html")
            
            # Send email
            email.send(fail_silently=False)
            
            return True
        
        except Exception as e:
            print(f"Error sending debit alert to {user.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_credit_alert(receiver_email, receiver_name, user, account, transfer):
        """
        Send credit alert email to the receiver.
        
        Args:
            receiver_email: Email address of receiver
            receiver_name: Name of receiver
            user: Django User object (sender)
            account: Account object (sender's account)
            transfer: Transfer object
        
        Returns:
            Boolean indicating success
        """
        try:
            # Create a temporary user-like object for receiver if needed
            context = TransactionEmailService.get_email_context(
                user, account, transfer, email_type='credit'
            )
            
            # Update context for receiver
            receiver_full_name = receiver_name
            context.update({
                'user_name': receiver_full_name,
                'sender_name': f"{user.first_name} {user.last_name}".strip() or user.email,
                'sender_bank': transfer.receiver_bank,
            })
            
            # Render HTML template
            html_message = render_to_string(
                'emails/transaction_credit.html',
                context
            )
            
            # Create email
            subject = f"Credit Alert: {TransactionEmailService.CURRENCY}{context['amount']} received"
            email = EmailMultiAlternatives(
                subject=subject,
                body=TransactionEmailService._get_plain_text_version(context, 'credit'),
                from_email=f"noreply@{TransactionEmailService.BANK_NAME.lower().replace(' ', '')}.com",
                to=[receiver_email]
            )
            
            # Attach HTML version
            email.attach_alternative(html_message, "text/html")
            
            # Send email
            email.send(fail_silently=False)
            
            return True
        
        except Exception as e:
            print(f"Error sending credit alert to {receiver_email}: {str(e)}")
            return False
    
    @staticmethod
    def _get_plain_text_version(context, email_type):
        """
        Generate a plain text version of the email for clients that don't support HTML.
        
        Args:
            context: Template context
            email_type: 'debit' or 'credit'
        
        Returns:
            Plain text email body
        """
        if email_type == 'debit':
            return f"""
DEBIT ALERT - TRANSACTION CONFIRMATION

Hello {context['user_name']},

A transfer has been successfully processed from your account.

TRANSACTION DETAILS:
Amount Debited: {context['currency']} {context['amount']}
Transfer Type: {context['transfer_type']}
Recipient Name: {context['receiver_name']}
Recipient Bank: {context['receiver_bank']}
Account Number: {context['receiver_account_number']}
Description: {context['description']}
Date & Time: {context['transaction_date']}
Transaction ID: {context['transaction_id']}

UPDATED BALANCE:
Available Balance: {context['currency']} {context['available_balance']}
Total Balance: {context['currency']} {context['total_balance']}

SECURITY NOTICE:
If you did not authorize this transfer or notice suspicious activity, 
please contact our customer support immediately at {context['support_email']} 
or call {context['support_phone']}.

© {context['current_year']} {context['bank_name']}. All rights reserved.
This is an automated message. Please do not reply to this email.
"""
        else:  # credit
            return f"""
CREDIT ALERT - MONEY RECEIVED

Hello {context['user_name']},

Great news! You have successfully received a transfer to your account.

{context['currency']} {context['amount']} RECEIVED!

SENDER INFORMATION:
Name: {context['sender_name']}
Bank: {context['sender_bank']}

TRANSACTION DETAILS:
Amount Credited: {context['currency']} {context['amount']}
Transfer Type: {context['transfer_type']}
Description/Note: {context['description']}
Date & Time: {context['transaction_date']}
Transaction ID: {context['transaction_id']}

UPDATED BALANCE:
Available Balance: {context['currency']} {context['available_balance']}
Total Balance: {context['currency']} {context['total_balance']}

SECURITY NOTICE:
If you did not expect this transfer or notice anything unusual, 
please contact our customer support immediately at {context['support_email']} 
or call {context['support_phone']}.

© {context['current_year']} {context['bank_name']}. All rights reserved.
This is an automated message. Please do not reply to this email.
"""
