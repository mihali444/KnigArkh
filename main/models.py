import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from book.validators import validate_file_size, validate_image_extension


class MainPageList(models.Model):
    """
    Модель для отображения объявлений на главной странице.
    
    Атрибуты:
        book_offer (BookOffer): Связь с объявлением
        type (str): Тип отображения на главной странице (популярное, новое, избранное)
    """
    class BookType(models.TextChoices):
        """Типы отображения книг на главной странице"""
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
    """
    Модель объявления о продаже книги.
    
    Атрибуты:
        user (User): Пользователь, создавший объявление
        uuid_post (UUID): Уникальный идентификатор объявления
        book (Book): Связь с моделью книги
        description (str): Описание объявления (максимум 3000 символов)
        is_published (bool): Статус публикации объявления
        is_active (str): Статус активности объявления
        edition_year (int): Год издания книги
        address (str): Адрес объявления (необязательно)
        date_created (datetime): Дата создания объявления
        date_updated (datetime): Дата последнего обновления объявления
    """
    class OfferStatus(models.TextChoices):
        """Статусы объявления"""
        ACTIVE = 'Active', 'Активное'
        COMPLETED = 'Completed', 'Завершенное'

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    uuid_post = models.UUIDField(
        default=uuid.uuid4,
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
    is_active = models.TextField(
        choices=OfferStatus.choices,
        default=OfferStatus.ACTIVE,
        verbose_name='Статус объявления'
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
    """
    Модель фотографии объявления.
    
    Атрибуты:
        book (BookOffer): Связь с объявлением
        image (ImageField): Изображение объявления
    """
    book = models.ForeignKey(
        to='BookOffer',
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Товар'
    )
    image = models.ImageField(
        upload_to='book/book_offers/%Y/%m/%d/',
        verbose_name='Фото',
        validators=[validate_file_size, validate_image_extension]
    )

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
