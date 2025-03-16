from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError


class Author(models.Model):
    name = models.CharField(
        max_length=150,
        db_index=True,
        verbose_name='Имя автора',
        help_text='Введите имя автора'
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
    description = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.author.name})"

    def clean(self):
        if len(self.title) < 3:
            raise ValidationError({'title': 'Название книги должно содержать минимум 3 символа.'})


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
