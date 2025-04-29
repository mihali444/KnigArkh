from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'date_of_birth', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'profile-edit__input profile-edit__input-name'}),
            'last_name': forms.TextInput(attrs={'class': 'profile-edit__input profile-edit__input-lastname'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'profile-edit__input',
                                                    'type': 'date',
                                                    'value': lambda x: x.isoformat() if x else ''},
                                             format='%Y-%m-%d'),
            'username': forms.TextInput(attrs={'class': 'profile-edit__input'}),
        }
