from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={
            'class': 'form__email',
            'placeholder': 'Электронная почта',
            'required': True
        })
    )
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            'class': 'form__username',
            'placeholder': 'Имя пользователя',
            'required': True
        })
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form__password',
            'placeholder': 'Пароль',
            'required': True,
            'id': 'password1'
        })
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form__password',
            'placeholder': 'Повторите пароль',
            'required': True,
            'id': 'password2'
        })
    )
    agree = forms.BooleanField(
        label="Я согласен с условиями обслуживания и политикой конфиденциальности",
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox__agree',
            'id': 'agree'
        }),
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'agree']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email


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
