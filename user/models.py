import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def validate_birth_date(value):
    min_date = datetime.date(1950, 1, 1)
    today = datetime.date.today()

    age = relativedelta(today, value).years

    if value < min_date:
        raise ValidationError('Дата рождения не может быть раньше 1 января 1950 года.')
    if age < 16:
        raise ValidationError('Вы должны быть старше 16 лет.')


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
        verbose_name='Дата рождения',
        validators=[validate_birth_date],
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        related_name='favorites',
        verbose_name='Пользователь'
    )
    offer = models.ForeignKey(
        'main.BookOffer', 
        on_delete=models.CASCADE,
        verbose_name='Объявление'
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'offer')
        ordering = ['-added_at']  # Most recently added first


class Reviews(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='От пользователя',
        related_name='reviews',
        help_text='Пользователь, оставивший отзыв'
    )
    offer = models.ForeignKey(
        to='main.BookOffer',
        on_delete=models.CASCADE,
        verbose_name='Объявление',
        related_name='reviews',
        help_text='Объявление, на которое оставлен отзыв'
    )
    grade = models.IntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        blank=True,
        help_text='Оценка от 0 до 5'
    )
    description = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        help_text='Текстовый отзыв (необязательно)'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('user', 'offer')
        ordering = ['-id']

    def __str__(self):
        """String representation of the review."""
        return f'Отзыв от {self.user.username} на {self.offer}'


class Subscriber(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',  # Подписки (кто подписан)
        verbose_name='Подписчик',
    )
    subscribed_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',  # Подписчики (у кого есть подписчики)
        verbose_name='Подписан на',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подписки',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('subscriber', 'subscribed_to')  # Уникальность пары подписчик-подписка
        constraints = [
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('subscribed_to')),
                name='prevent_self_subscription'
            )
        ]

    def __str__(self):
        return f"{self.subscriber.username} -> {self.subscribed_to.username}"

