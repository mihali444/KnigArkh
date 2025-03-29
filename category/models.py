from django.db import models


# Create your models here.
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

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
