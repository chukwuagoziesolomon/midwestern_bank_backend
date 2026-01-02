from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Transfer, CreditCardDeposit, Account

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['id', 'transfer_type', 'receiver_name', 'receiver_bank', 'receiver_account_number', 'routing_number', 'receiver_bank_address', 'iban', 'swift_code', 'amount', 'description', 'pin', 'date', 'status']
        read_only_fields = ['id', 'date', 'status']

    def validate(self, data):
        transfer_type = data.get('transfer_type')
        if transfer_type == 'local':
            if not data.get('routing_number'):
                raise serializers.ValidationError("Routing number is required for local transfers.")
        elif transfer_type == 'international':
            required_fields = ['receiver_bank_address', 'iban', 'swift_code']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f"{field} is required for international transfers.")
        pin = data.get('pin')
        if pin != '2027':
            raise serializers.ValidationError("Invalid PIN.")
        return data

class CreditCardDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardDeposit
        fields = ['id', 'card_number', 'card_expiry', 'card_cvc', 'deposit_amount', 'card_holder_name', 'date', 'status']
        read_only_fields = ['id', 'date', 'status']

    def validate(self, data):
        # Validation moved to view to check against user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['total_balance', 'available_balance', 'loans_due', 'mortgage_due']