from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer, LoginSerializer, TransferSerializer, CreditCardDepositSerializer, UserSerializer, ChangePasswordSerializer, AccountSerializer, AdminUserListSerializer, AdminUserDetailSerializer
from .models import Transfer, Account, CreditCardDeposit
from .services import TransactionEmailService
from .transaction_generator import DummyTransactionGenerator
from django.utils import timezone
from decimal import Decimal, InvalidOperation
import random
import string
from django.http import HttpResponse
from django.template.loader import render_to_string
import io
try:
    from xhtml2pdf import pisa
except Exception:
    pisa = None
from django.urls import reverse
try:
    import imgkit
except Exception:
    imgkit = None

# Create your views here.

class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Use password provided by user
            password = serializer.validated_data['password']
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=password,
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
            
            # Send welcome email with credentials
            try:
                from django.core.mail import send_mail
                full_name = f"{user.first_name} {user.last_name}"
                subject = 'Welcome to Midwestern Bank - Your Account Created'
                message = f"""
Hello {full_name},

Welcome to Midwestern Bank! Your account has been created successfully.

Your Account Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Email: {email}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Next Steps:
1. Wait for admin approval (you'll receive an email confirmation)
2. Once approved, login to your account using your email and password
3. You'll receive a $70,000 balance + transaction history

⚠️  Important:
- Your account is currently pending admin approval
- Only approved accounts can login
- Keep your credentials safe and secure
- Do not share your password with anyone

If you have any questions, contact us at support@midwesternbank.com

Best regards,
Midwestern Bank Team
                """
                send_mail(
                    subject,
                    message,
                    'noreply@midwesternbank.com',
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
            
            return Response({
                'message': 'User created successfully. Check your email for confirmation.',
                'email': email,
                'status': 'pending_approval',
                'note': 'A confirmation email has been sent. Your account is pending admin approval.'
            }, status=status.HTTP_201_CREATED)
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
                transfer = serializer.save(user=user)
                if account.available_balance >= transfer.amount:
                    account.available_balance -= transfer.amount
                    account.transfer_count += 1
                    account.save()
                    transfer.status = 'completed'
                    transfer.save()

                    # Send debit alert to sender (user)
                    TransactionEmailService.send_debit_alert(user, account, transfer)

                    # Send credit alert to receiver
                    receiver_email = request.data.get('receiver_email')
                    if receiver_email:
                        TransactionEmailService.send_credit_alert(
                            receiver_email,
                            transfer.receiver_name,
                            user,
                            account,
                            transfer
                        )

                    # Build receipt URLs for frontend modal
                    html_url = request.build_absolute_uri(reverse('transfer-receipt', args=[transfer.id])) + f"?user_id={user.id}"
                    pdf_url = request.build_absolute_uri(reverse('transfer-receipt-pdf', args=[transfer.id])) + f"?user_id={user.id}"
                    image_url = request.build_absolute_uri(reverse('transfer-receipt-image', args=[transfer.id])) + f"?user_id={user.id}"

                    return Response({'message': 'Transfer created successfully', 'transfer': serializer.data, 'receipt_urls': {'html': html_url, 'pdf': pdf_url, 'image': image_url}}, status=status.HTTP_201_CREATED)
                else:
                    transfer.status = 'failed'
                    transfer.save()
                    return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class TransferReceiptView(APIView):
    """Return a downloadable receipt (HTML) for a transfer."""

    def get(self, request, transfer_id):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            try:
                transfer = Transfer.objects.get(id=transfer_id)
            except Transfer.DoesNotExist:
                return Response({'error': 'Transfer not found'}, status=status.HTTP_404_NOT_FOUND)

            # Ensure the transfer belongs to the requesting user
            if transfer.user_id != user.id:
                return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            account = Account.objects.get(user=user)

            # Build context using existing service (same as email)
            context = TransactionEmailService.get_email_context(user, account, transfer, email_type='debit')

            rendered = render_to_string('receipts/transfer_receipt.html', context)

            filename = f"{context['transaction_id']}_receipt.html"
            response = HttpResponse(rendered, content_type='text/html; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)


class TransferReceiptPDFView(APIView):
    """Return a downloadable PDF receipt for a transfer."""

    def get(self, request, transfer_id):
        if pisa is None:
            return Response({'error': 'PDF generation library not installed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            try:
                transfer = Transfer.objects.get(id=transfer_id)
            except Transfer.DoesNotExist:
                return Response({'error': 'Transfer not found'}, status=status.HTTP_404_NOT_FOUND)

            if transfer.user_id != user.id:
                return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            account = Account.objects.get(user=user)
            context = TransactionEmailService.get_email_context(user, account, transfer, email_type='debit')
            html = render_to_string('receipts/transfer_receipt.html', context)

            result = io.BytesIO()
            pdf = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=result)
            if pdf.err:
                return Response({'error': 'Failed to generate PDF'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            pdf_bytes = result.getvalue()
            filename = f"{context['transaction_id']}_receipt.pdf"
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

class TransferReceiptImageView(APIView):
    """Return a downloadable PNG receipt for a transfer."""

    def get(self, request, transfer_id):
        if imgkit is None:
            return Response({'error': 'Image generation library not installed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            try:
                transfer = Transfer.objects.get(id=transfer_id)
            except Transfer.DoesNotExist:
                return Response({'error': 'Transfer not found'}, status=status.HTTP_404_NOT_FOUND)

            if transfer.user_id != user.id:
                return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            account = Account.objects.get(user=user)
            context = TransactionEmailService.get_email_context(user, account, transfer, email_type='debit')
            html = render_to_string('receipts/transfer_receipt.html', context)

            try:
                img_bytes = imgkit.from_string(html, False, options={'format': 'png'})
            except Exception as e:
                return Response({'error': f'Failed to generate image: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            filename = f"{context['transaction_id']}_receipt.png"
            response = HttpResponse(img_bytes, content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

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
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            # Ensure UserProfile exists
            from .models_profile import UserProfile
            UserProfile.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user_id = request.data.get('user_id') or request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
            from .models_profile import UserProfile
            profile, _ = UserProfile.objects.get_or_create(user=user)
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                image = request.FILES['profile_picture']
                # Upload to Cloudinary
                import cloudinary.uploader
                result = cloudinary.uploader.upload(image)
                profile.profile_picture = result.get('secure_url')
                profile.save()
                return Response({'profile_picture': profile.profile_picture}, status=status.HTTP_200_OK)
            # Otherwise, handle password change as before
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
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                
                # Auto-create Account if it doesn't exist (for superusers)
                account, created = Account.objects.get_or_create(
                    user=user,
                    defaults={
                        'generated_card_number': ''.join(random.choices('0123456789', k=16)),
                        'generated_expiry': f"{random.randint(1,12):02d}/{random.randint(25,30)}",
                        'generated_cvc': ''.join(random.choices('0123456789', k=3)),
                        'is_approved': user.is_superuser  # Auto-approve superusers
                    }
                )
                
                # Check if account is approved
                if not account.is_approved:
                    return Response(
                        {'error': 'Your account is not yet approved. Please wait for admin approval.'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                if user.check_password(password):
                    return Response({
                        'message': 'Login successful', 
                        'user': {
                            'id': user.id, 
                            'email': user.email, 
                            'first_name': user.first_name, 
                            'last_name': user.last_name,
                            'is_approved': account.is_approved,
                            'is_superuser': user.is_superuser
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================== ADMIN ENDPOINTS ====================

class AdminUserListView(APIView):
    """List all users with their approval status for admin dashboard"""
    
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = AdminUserListSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminUserDetailView(APIView):
    """Get detailed info about a specific user"""
    
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = AdminUserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminApproveUserView(APIView):
    """Approve/Activate a user account for login with optional custom transaction date range"""
    
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            account = Account.objects.get(user=user)
            
            action = request.data.get('action', 'approve')  # 'approve' or 'reject'
            
            if action == 'approve':
                account.is_approved = True
                account.save()
                
                # Get optional custom date range from request
                start_date = request.data.get('start_date', None)  # Format: YYYY-MM-DD
                end_date = request.data.get('end_date', None)      # Format: YYYY-MM-DD
                
                # Generate dummy transaction history when approving
                DummyTransactionGenerator.generate_transactions_for_user(
                    user, 
                    num_transactions=15,
                    start_date=start_date,
                    end_date=end_date
                )
                DummyTransactionGenerator.generate_deposit_history_for_user(
                    user, 
                    num_deposits=5,
                    start_date=start_date,
                    end_date=end_date
                )
                
                date_info = ""
                if start_date or end_date:
                    date_info = f" (Transactions from {start_date or 'Dec 1, 2023'} to {end_date or 'Today'})"
                
                return Response({
                    'message': f'User {user.email} has been approved and can now login. Transaction history generated{date_info}.',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'is_approved': account.is_approved,
                        'initial_balance': str(account.total_balance),
                        'transactions_generated': 15,
                        'start_date': start_date or '2023-12-01',
                        'end_date': end_date or 'Today'
                    }
                }, status=status.HTTP_200_OK)
            
            elif action == 'reject':
                account.is_approved = False
                account.save()
                return Response({
                    'message': f'User {user.email} has been rejected',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'is_approved': account.is_approved
                    }
                }, status=status.HTTP_200_OK)
            
            else:
                return Response({'error': 'Invalid action. Use "approve" or "reject"'}, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminResetTransfersView(APIView):
    """Reset transfer count for a user"""
    
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            account = Account.objects.get(user=user)
            
            # Reset transfer count
            account.transfer_count = 0
            account.save()
            
            return Response({
                'message': f'Transfer count reset for user {user.email}',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'transfer_count': account.transfer_count
                }
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminDeleteUserView(APIView):
    """Delete a user account completely"""
    
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            email = user.email
            user.delete()
            
            return Response({
                'message': f'User {email} has been deleted',
                'deleted_user_id': user_id
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminIncreaseBalanceView(APIView):
    """Increase account balance and available balance for a user"""
    
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            account = Account.objects.get(user=user)
            
            # Get the amount to increase from request
            increase_amount = request.data.get('amount', None)
            
            if not increase_amount:
                return Response({
                    'error': 'Amount is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                increase_amount = Decimal(str(increase_amount))
                if increase_amount <= 0:
                    return Response({
                        'error': 'Amount must be greater than 0'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except (ValueError, InvalidOperation):
                return Response({
                    'error': 'Invalid amount format'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Store old balances for response
            old_total_balance = account.total_balance
            old_available_balance = account.available_balance
            
            # Increase both balances
            account.total_balance += increase_amount
            account.available_balance += increase_amount
            account.save()
            
            return Response({
                'message': f'Successfully increased balance for {user.email}',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'increase_amount': str(increase_amount),
                    'old_total_balance': str(old_total_balance),
                    'new_total_balance': str(account.total_balance),
                    'old_available_balance': str(old_available_balance),
                    'new_available_balance': str(account.available_balance)
                }
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
