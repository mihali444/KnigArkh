from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy


# Create your views here.
class UserResetPasswordView(PasswordResetView):
    template_name = 'rest_password/password-reset.html'
    form_class = PasswordResetForm
    html_email_template_name = 'rest_password/password_reset_email.html'
    email_template_name = 'rest_password/password_reset_email.html'
    success_url = reverse_lazy('rest-password:password-reset-done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'rest_password/enter-email.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'rest_password/new-password.html'
    success_url = reverse_lazy('login')
