from django.contrib.auth.views import PasswordResetView
from django.urls import path

from user.views import UserLoginView, logout_views, UserRegisterView, toggle_favorite, UserResetPasswordView, \
    UserPasswordResetConfirmView, UseerPasswordResetDoneView

app_name = 'profile'

urlpatterns = [
    path('toggle-favorite/', toggle_favorite, name='toggle-favorite'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_views, name='logout'),
    path('registration/', UserRegisterView.as_view(), name='registration'),
    path('reset-password/', UserResetPasswordView.as_view(), name='reset-password'),
    path('password-reset/done/', UseerPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
