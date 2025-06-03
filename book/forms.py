from django import forms
from book.models import Author, Publisher, Book


class AuthorForm(forms.ModelForm):
    """
    Форма для создания и редактирования автора.
    
    Поля:
        name: Имя автора
        bio: Краткая биография автора
    """
    class Meta:
        model = Author
        fields = ['name', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


class PublisherForm(forms.ModelForm):
    """
    Форма для создания и редактирования издательства.
    
    Поля:
        name: Название издательства
    """
    class Meta:
        model = Publisher
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class BookForm(forms.ModelForm):
    """
    Форма для создания и редактирования книги.
    
    Поля:
        title: Название книги
        img: Фотография книги
        language: Язык книги
        category: Категории книги
        description: Описание книги
        release_year: Год выпуска
        publisher: Издательство
    """
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
