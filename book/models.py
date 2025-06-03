from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .validators import validate_file_size, validate_image_extension


class Author(models.Model):
    """
    Модель автора книги.
    
    Атрибуты:
        name (str): Имя автора (максимум 150 символов)
        bio (str): Краткая биография автора (необязательно, максимум 3000 символов)
    """
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Имя',
        help_text='Введите имя автора'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=3000,
        verbose_name='Краткая биография',
        help_text='Краткая биография автора(не обязательно)'
    )

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Модель книги.
    
    Атрибуты:
        title (str): Название книги (максимум 100 символов)
        img (ImageField): Фотография книги
        language (str): Язык книги (выбор из предопределенных языков)
        author (Author): Связь с моделью автора
        category (Category): Связь с категориями книги
        publisher (Publisher): Связь с издательством
        description (str): Описание книги (необязательно, максимум 3000 символов)
        release_year (int): Год выпуска книги (необязательно)
    """
    class Language(models.TextChoices):
        """Выбор языка книги"""
        ENG = 'Английский', 'en'
        RUS = 'Русский', 'ru'

    title = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Название книги',
        help_text='Введите название книги',
    )
    img = models.ImageField(
        blank=True,
        default='book/default_book/default.png',
        upload_to='book/default_book/',
        verbose_name='Фото',
        validators=[validate_file_size, validate_image_extension]
    )
    language = models.CharField(
        max_length=20,
        choices=Language.choices,
        verbose_name='Язык',
    )
    author = models.ForeignKey(
        to='Author',
        on_delete=models.CASCADE,
        related_name='authored_books',
        verbose_name='Автор',
        help_text='Выберите автора книги',
    )
    category = models.ManyToManyField(
        to='category.Category',
        related_name='categorized_books',
        # through='BookCategory',
        verbose_name='Категории',
        help_text='Выберите категории, к которым относится книга',
    )
    publisher = models.ForeignKey(
        to='Publisher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='published_books',
        verbose_name='Издатель',
        help_text='Выберите издателя книги',
    )
    description = models.TextField(
        max_length=3000,
        blank=True,
        null=True,
        verbose_name='Описание книги',
        help_text='Описание книги',
    )
    release_year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Год выпуска',
        validators=[MinValueValidator(1000), MaxValueValidator(datetime.now().year)],
    )

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f"{self.title} ({self.author.name} – {self.publisher})"

    def clean(self):
        """
        Валидация данных книги.
        
        Проверяет:
        - Длина названия книги (минимум 3 символа)
        - Наличие описания
        """
        if len(self.title) < 3:
            raise ValidationError({'title': 'Название книги должно содержать минимум 3 символа.'})
        if not self.description.strip():
            raise ValidationError({'description': 'Описание не может быть пустым.'})


class Photo(models.Model):
    """
    Модель фотографии книги.
    
    Атрибуты:
        book (Book): Связь с моделью книги
        image (ImageField): Изображение книги
    """
    book = models.ForeignKey(
        to='Book',
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Товар'
    )
    image = models.ImageField(
        upload_to='book/default_book/',
        verbose_name='Изображение',
        validators=[validate_file_size, validate_image_extension]
    )

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class Publisher(models.Model):
    """
    Модель издательства.
    
    Атрибуты:
        name (str): Название издательства (максимум 150 символов)
    """
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Название издателя',
        help_text='Введите название издателя'
    )

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'

    def __str__(self):
        return self.name
