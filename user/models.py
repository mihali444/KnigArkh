from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(
        upload_to='users/profile_pictures/%Y/%m',
        blank=True,
        verbose_name='Фото профиля',
        default='users/profile_pictures/default.png',
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    # rating = models.FloatField()


class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorites')
    offer = models.ForeignKey('main.BookOffer', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'offer')


class Reviews(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='От пользователя',
        related_name='reviews'
    )
    offer = models.ForeignKey(
        to='main.BookOffer',
        on_delete=models.CASCADE,
        verbose_name='Объявление',
        related_name='reviews'
    )
    grade = models.IntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        blank=True,
    )
    description = models.TextField(
        verbose_name='Комментарий',
        blank=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('user', 'offer')
