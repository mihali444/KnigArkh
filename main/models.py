import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MainPageList(models.Model):
    """ Таблица: Главная страница """
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
        choices=BookType.choices,
        verbose_name='Тип книги'
    )

    class Meta:
        verbose_name = 'Объявление на главной странице'
        verbose_name_plural = 'Объявления на главной странице'

    def __str__(self):
        return f"{self.book_offer} ({self.type})"


class BookOffer(models.Model):
    """ Таблица: Объявления """

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    uuid_post = models.UUIDField(
        default=uuid.uuid4,
        # editable=False,
    )
    book = models.ForeignKey(
        to='book.Book',
        on_delete=models.CASCADE,
        verbose_name='Книга',
        related_name='book_offers',
    )
    description = models.TextField(
        max_length=3000,
        verbose_name='Описание объявления',
        help_text='Описание объявления'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовать'
    )
    edition_year = models.IntegerField(
        verbose_name='Год издания книги',
        validators=[MinValueValidator(1000), MaxValueValidator(2100)]
    )
    address = models.TextField(
        max_length=250,
        verbose_name='Адрес объявления',
        help_text='Адрес объявления',
        blank=True,
        null=True
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания объявления',
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения объявления'
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return f"{self.user} ({self.book})"


class Photo(models.Model):
    """ Таблица: Фотографии объявления """
    book = models.ForeignKey(
        to='BookOffer',
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Товар'
    )
    image = models.ImageField(
        upload_to='book/book_offers/%Y/%m/%d/',
        verbose_name='Фото',
    )

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
