from django.urls import path
from rest_password.views import UserPasswordResetDoneView, UserPasswordResetConfirmView, UserResetPasswordView

app_name = 'rest-password'

urlpatterns = [
    path('', UserResetPasswordView.as_view(), name='reset-password'),
    path('password-reset/done/', UserPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]