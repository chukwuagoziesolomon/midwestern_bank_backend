from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=70000.00)
    available_balance = models.DecimalField(max_digits=15, decimal_places=2, default=70000.00)
    loans_due = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    mortgage_due = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    transfer_count = models.IntegerField(default=0)
    generated_card_number = models.CharField(max_length=16, blank=True, null=True)
    generated_expiry = models.CharField(max_length=5, blank=True, null=True)  # MM/YY
    generated_cvc = models.CharField(max_length=3, blank=True, null=True)
    is_approved = models.BooleanField(default=False)  # Admin approval for login
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Total: {self.total_balance}, Available: {self.available_balance}"

class CreditCardDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_expiry = models.CharField(max_length=5)
    card_cvc = models.CharField(max_length=3)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_holder_name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')

    def __str__(self):
        return f"Deposit - {self.deposit_amount} - {self.user.email}"

class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transfer_type = models.CharField(max_length=15, choices=[('local', 'Local'), ('international', 'International')])
    receiver_name = models.CharField(max_length=255)
    receiver_bank = models.CharField(max_length=255)
    receiver_account_number = models.CharField(max_length=50)
    routing_number = models.CharField(max_length=50, blank=True, null=True)  # For local
    receiver_bank_address = models.TextField(blank=True, null=True)  # For international
    iban = models.CharField(max_length=50, blank=True, null=True)  # For international
    swift_code = models.CharField(max_length=50, blank=True, null=True)  # For international
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    pin = models.CharField(max_length=10)  # Assuming pin is stored, but in real app, verify
    date = models.DateTimeField(default=timezone.now)  # Allow custom dates for historical transactions
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')

    def __str__(self):
        return f"{self.transfer_type} Transfer - {self.amount} - {self.user.email}"
