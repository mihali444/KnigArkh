from django import forms
from book.models import Author, Publisher, Book


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


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'img', 'language', 'category', 'description', 'release_year', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'new-advertisement__input', 'placeholder': 'Введите название книги'}),
            'language': forms.Select(attrs={'class': 'new-advertisement__input'}),
            'description': forms.Textarea(attrs={'class': 'new-advertisement__textarea'}),
            'release_year': forms.NumberInput(attrs={'class': 'new-advertisement__input', 'placeholder': 'Введите год выпуска...'}),
            'publisher': forms.Select(attrs={'class': 'new-advertisement__input'}),
        }
