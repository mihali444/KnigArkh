from django import forms
from book.models import Author, Publisher


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }
