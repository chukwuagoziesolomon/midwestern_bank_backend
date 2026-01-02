from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer, LoginSerializer, TransferSerializer, CreditCardDepositSerializer, UserSerializer, ChangePasswordSerializer, AccountSerializer
from .models import Transfer, Account, CreditCardDeposit
from django.utils import timezone
import random
import string

# Create your views here.

class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            # Generate fake password for all users
            fake_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=fake_password,
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name']
            )
            # Generate fake card details for all users
            card_number = ''.join(random.choices('0123456789', k=16))
            expiry = f"{random.randint(1,12):02d}/{random.randint(25,30)}"
            cvc = ''.join(random.choices('0123456789', k=3))
            Account.objects.create(
                user=user,
                generated_card_number=card_number,
                generated_expiry=expiry,
                generated_cvc=cvc
            )
            return Response({'message': 'User created successfully', 'password': fake_password}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransferView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            transfers = Transfer.objects.filter(user=user).order_by('-date')
            serializer = TransferSerializer(transfers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            account = Account.objects.get(user=user)
            if account.transfer_count >= 2:
                return Response({'error': 'Transfer quota exceeded'}, status=status.HTTP_400_BAD_REQUEST)
            data = request.data.copy()
            data['user'] = user.id
            serializer = TransferSerializer(data=data)
            if serializer.is_valid():
                transfer = serializer.save()
                if account.available_balance >= transfer.amount:
                    account.available_balance -= transfer.amount
                    account.transfer_count += 1
                    account.save()
                    transfer.status = 'completed'
                    transfer.save()
                    return Response({'message': 'Transfer created successfully', 'transfer': serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    transfer.status = 'failed'
                    transfer.save()
                    return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class CreditCardDepositView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            account = Account.objects.get(user=user)
            data = request.data.copy()
            data['user'] = user.id
            serializer = CreditCardDepositSerializer(data=data)
            if serializer.is_valid():
                card_holder_name = serializer.validated_data['card_holder_name'].lower()
                user_full_name = f"{user.first_name.lower()} {user.last_name.lower()}"
                if card_holder_name != user_full_name:
                    return Response({'error': 'Card holder name does not match user name'}, status=status.HTTP_400_BAD_REQUEST)
                card_number = serializer.validated_data['card_number']
                card_expiry = serializer.validated_data['card_expiry']
                card_cvc = serializer.validated_data['card_cvc']
                if (card_number == account.generated_card_number and
                    card_expiry == account.generated_expiry and
                    card_cvc == account.generated_cvc):
                    deposit = serializer.save()
                    # Add to balance
                    account.total_balance += deposit.deposit_amount
                    account.available_balance += deposit.deposit_amount
                    account.save()
                    deposit.status = 'completed'
                    deposit.save()
                    return Response({'message': 'Deposit successful', 'deposit': serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    deposit = serializer.save()
                    deposit.status = 'failed'
                    deposit.save()
                    return Response({'error': 'Invalid card details'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

class UserSettingsView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                current_password = serializer.validated_data['current_password']
                new_password = serializer.validated_data['new_password']
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class DashboardView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            account = Account.objects.get(user=user)
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

class CardView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            account = Account.objects.get(user=user)
            if account.generated_card_number:
                return Response({
                    'card_holder_name': f"{user.first_name} {user.last_name}",
                    'card_number': account.generated_card_number,
                    'card_expiry': account.generated_expiry,
                    'card_cvc': account.generated_cvc
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No card details available'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return Response({'message': 'Login successful', 'user': {'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
