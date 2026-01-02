from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('transfers/', views.TransferView.as_view(), name='transfers'),
    path('deposit/', views.CreditCardDepositView.as_view(), name='deposit'),
    path('settings/', views.UserSettingsView.as_view(), name='settings'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('card/', views.CardView.as_view(), name='card'),
]