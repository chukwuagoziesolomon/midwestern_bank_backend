"""
Management command to create an admin/superuser account
Usage: python manage.py create_admin
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bankapp.models import Account
import random


class Command(BaseCommand):
    help = 'Create an admin/superuser account for Midwestern Bank'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Admin email address')
        parser.add_argument('--password', type=str, help='Admin password')
        parser.add_argument('--first-name', type=str, default='Admin', help='Admin first name')
        parser.add_argument('--last-name', type=str, default='User', help='Admin last name')

    def handle(self, *args, **options):
        email = options.get('email') or input('Enter admin email: ')
        password = options.get('password') or input('Enter admin password: ')
        first_name = options.get('first_name', 'Admin')
        last_name = options.get('last_name', 'User')

        # Check if admin already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Admin with email {email} already exists'))
            return

        try:
            # Create superuser
            admin_user = User.objects.create_superuser(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create admin account
            card_number = ''.join(random.choices('0123456789', k=16))
            expiry = f"{random.randint(1,12):02d}/{random.randint(25,30)}"
            cvc = ''.join(random.choices('0123456789', k=3))
            
            Account.objects.create(
                user=admin_user,
                generated_card_number=card_number,
                generated_expiry=expiry,
                generated_cvc=cvc,
                is_approved=True  # Admin is automatically approved
            )

            self.stdout.write(self.style.SUCCESS(f'✓ Admin account created successfully!'))
            self.stdout.write(self.style.SUCCESS(f'  Email: {email}'))
            self.stdout.write(self.style.SUCCESS(f'  Status: Superuser & Approved'))
            self.stdout.write(self.style.SUCCESS(f'  Initial Balance: $70,000'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating admin: {str(e)}'))
