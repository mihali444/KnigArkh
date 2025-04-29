from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            'class': 'form__email',
            'placeholder': 'Имя пользователя',
            'required': True
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form__password',
            'placeholder': 'Пароль',
            'required': True,
            'id': 'password'
        })
    )
