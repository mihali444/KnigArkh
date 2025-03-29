from django import forms

from main.models import BookOffer


class BookOfferForm(forms.Form):
    class Meta:
        model = BookOffer
        fields = ['book', 'description', 'language', 'publisher', 'edition_year', 'address']
        widgets = {}
