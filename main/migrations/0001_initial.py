# Generated by Django 3.2.16 on 2025-03-25 16:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid_post', models.UUIDField(default=uuid.uuid4)),
                ('description', models.TextField(help_text='Описание объявления', max_length=3000, verbose_name='Описание объявления')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовать')),
                ('edition_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(2100)], verbose_name='Год издания книги')),
                ('address', models.TextField(blank=True, help_text='Адрес объявления', max_length=250, null=True, verbose_name='Адрес объявления')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания объявления')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Дата изменения объявления')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_offers', to='book.book', verbose_name='Книга')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='book/book_offers/%Y/%m/%d/', verbose_name='Фото')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='main.bookoffer', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
            },
        ),
        migrations.CreateModel(
            name='MainPageList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('popular', 'Популярная'), ('new', 'Новая'), ('featured', 'Избранная')], max_length=20, verbose_name='Тип книги')),
                ('book_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_page_lists', to='main.bookoffer', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'Объявление на главной странице',
                'verbose_name_plural': 'Объявления на главной странице',
            },
        ),
    ]
