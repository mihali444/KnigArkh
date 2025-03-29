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
