from django.urls import path
from . import views

urlpatterns = [
    # User Endpoints
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('transfers/', views.TransferView.as_view(), name='transfers'),
    path('deposit/', views.CreditCardDepositView.as_view(), name='deposit'),
    path('settings/', views.UserSettingsView.as_view(), name='settings'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('card/', views.CardView.as_view(), name='card'),
    
    # Admin Endpoints
    path('admin/users/', views.AdminUserListView.as_view(), name='admin-users-list'),
    path('admin/users/<int:user_id>/', views.AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/users/<int:user_id>/approve/', views.AdminApproveUserView.as_view(), name='admin-approve-user'),
    path('admin/users/<int:user_id>/reset-transfers/', views.AdminResetTransfersView.as_view(), name='admin-reset-transfers'),
    path('admin/users/<int:user_id>/delete/', views.AdminDeleteUserView.as_view(), name='admin-delete-user'),
]