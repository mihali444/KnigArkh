from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, Reviews


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя.
    
    Поля:
        username: Имя пользователя
        email: Email пользователя
        password1: Пароль
        password2: Подтверждение пароля
        first_name: Имя
        last_name: Фамилия
        date_of_birth: Дата рождения
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'})
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        }

    def clean_email(self):
        """
        Проверяет уникальность email.
        
        Returns:
            str: Очищенный email
            
        Raises:
            forms.ValidationError: Если email уже используется
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email


class UserLoginForm(AuthenticationForm):
    """
    Форма входа пользователя в систему.
    
    Поля:
        username: Имя пользователя
        password: Пароль
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )


class ProfileEditForm(forms.ModelForm):
    """
    Форма редактирования профиля пользователя.
    
    Поля:
        username: Имя пользователя
        email: Email пользователя
        first_name: Имя
        last_name: Фамилия
        date_of_birth: Дата рождения
        photo: Фотография профиля
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'photo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        """
        Проверяет уникальность email.
        
        Returns:
            str: Очищенный email
            
        Raises:
            forms.ValidationError: Если email уже используется другим пользователем
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email


class ReviewForm(forms.ModelForm):
    """
    Форма для создания отзыва.
    
    Поля:
        grade: Оценка (от 0 до 5)
        description: Текстовый отзыв
    """
    class Meta:
        model = Reviews
        fields = ['grade', 'description']
        widgets = {
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 5}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
