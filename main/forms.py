from django import forms

from main.models import BookOffer


class BookOfferForm(forms.ModelForm):
    class Meta:
        model = BookOffer
        fields = ['book', 'description', 'edition_year', 'address']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'new-advertisement__textarea', 'id': 'seller-description'}),
            'edition_year': forms.NumberInput(attrs={'class': 'new-advertisement__input', 'placeholder': 'Введите год издания...'}),
            'address': forms.TextInput(attrs={'class': 'new-advertisement__input location-input', 'placeholder': 'Ваше местоположение'}),
        }
