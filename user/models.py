from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
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
