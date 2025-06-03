from django import forms
from django.forms import inlineformset_factory

from main.models import BookOffer, Photo


class BookOfferForm(forms.ModelForm):
    """
    Форма для создания и редактирования объявления о книге.
    
    Поля:
        book: Выбор книги из каталога
        description: Описание объявления (максимум 3000 символов)
        edition_year: Год издания книги
        address: Адрес объявления (необязательно)
        is_published: Флаг публикации объявления
        is_active: Статус объявления (активное/завершенное)
    """
    class Meta:
        model = BookOffer
        fields = ['book', 'description', 'edition_year', 'address', 'is_published', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


# Создаем набор форм для загрузки фотографий
PhotoFormSet = inlineformset_factory(
    BookOffer,
    Photo,
    fields=['image'],
    extra=1,
    can_delete=True,
    max_num=5,
    validate_max=True,
    min_num=1,
    validate_min=True
)
