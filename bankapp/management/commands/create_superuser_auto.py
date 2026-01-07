"""
Management command to auto-create a superuser from environment variables
Usage: python manage.py create_superuser_auto

Environment variables (optional):
- ADMIN_EMAIL: Admin email (default: admin@midwesternbank.com)
- ADMIN_PASSWORD: Admin password (default: AdminPassword123!)
- ADMIN_FIRST_NAME: Admin first name (default: Admin)
- ADMIN_LAST_NAME: Admin last name (default: User)
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bankapp.models import Account
import os
import random


class Command(BaseCommand):
    help = 'Auto-create a superuser from environment variables (for deployment)'

    def handle(self, *args, **options):
        # Get admin credentials from environment or use defaults
        email = os.getenv('ADMIN_EMAIL', 'admin@midwesternbank.com')
        password = os.getenv('ADMIN_PASSWORD', 'AdminPassword123!')
        first_name = os.getenv('ADMIN_FIRST_NAME', 'Admin')
        last_name = os.getenv('ADMIN_LAST_NAME', 'User')

        # Check if admin already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.SUCCESS(f'✅ Admin already exists: {email}')
            )
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
                is_approved=True  # Admin accounts are auto-approved
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Superuser created successfully!\n'
                    f'   Email: {email}\n'
                    f'   Password: {password}\n'
                    f'   Name: {first_name} {last_name}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating superuser: {str(e)}')
            )
