from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError


class MainPageList(models.Model):
    class BookType(models.TextChoices):
        POPULAR = 'popular', 'Популярная'
        NEW = 'new', 'Новая'
        FEATURED = 'featured', 'Избранная'

    book_offer = models.ForeignKey(
        to='BookOffer',
        on_delete=models.CASCADE,
        verbose_name='Объявление',
        related_name='main_page_lists',
    )
    type = models.CharField(
        max_length=20,
        choices=BookType,
        verbose_name='Тип книги'
    )

    def __str__(self):
        return f"{self.book_offer} ({self.type})"


class BookOffer(models.Model):
    class Language(models.TextChoices):
        ENG = 'en', 'Английский'
        RUS = 'rus', 'Русский'

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    book = models.ForeignKey(
        to='Book',
        on_delete=models.CASCADE,
        verbose_name='Книга',
        related_name='book_offers',
    )
    description = models.TextField(
        max_length=3000,
        verbose_name='Описание объявления',
        help_text='Описание объявления'
    )
    language = models.CharField(
        max_length=20,
        choices=Language,
        verbose_name='Язык',
    )
    edition_year = models.IntegerField(
        verbose_name='Год издания книги',
        validators=[MinValueValidator(1000), MaxValueValidator(2100)]
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания объявления',
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения объявления'
    )


class Author(models.Model):
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Имя автора',
        help_text='Введите имя автора'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=3000,
        verbose_name='Краткая биография автора',
        help_text='Краткая биография автора(не обязательно)'
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Название категории',
        help_text='Введите название категории'
    )
    img = models.ImageField(
        upload_to='images/category/',
        verbose_name='Фото категории',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Название книги',
        help_text='Введите название книги'
    )
    author = models.ForeignKey(
        to='Author',
        on_delete=models.CASCADE,
        related_name='authored_books',
        verbose_name='Автор',
        help_text='Выберите автора книги'
    )
    category = models.ManyToManyField(
        'Category',
        related_name='categorized_books',
        through='BookCategory',
        verbose_name='Категории',
        help_text='Выберите категории, к которым относится книга'
    )
    publisher = models.ForeignKey(
        to='Publisher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='published_books',
        verbose_name='Издатель',
        help_text='Выберите издателя книги'
    )
    description = models.TextField(
        max_length=3000,
        blank=True,
        null=True,
        verbose_name='Описание книги',
        help_text='Описание книги'
    )
    release_year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Год выпуска',
        validators=[MinValueValidator(1000), MaxValueValidator(2100)]
    )

    def __str__(self):
        return f"{self.title} ({self.author.name})"

    def clean(self):
        if len(self.title) < 3:
            raise ValidationError({'title': 'Название книги должно содержать минимум 3 символа.'})
        if not self.description.strip():
            raise ValidationError({'description': 'Описание не может быть пустым.'})


class Publisher(models.Model):
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Название издателя',
        help_text='Введите название издателя'
    )

    def __str__(self):
        return self.name


class BookCategory(models.Model):
    book = models.ForeignKey(
        to='Book',
        on_delete=models.CASCADE,
        verbose_name='Книга'
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    def __str__(self):
        return f"{self.book.title} - {self.category.name}"
