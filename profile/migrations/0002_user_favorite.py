# Generated by Django 5.1.7 on 2025-03-30 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_bookoffer_user'),
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='offer_user', to='main.bookoffer', verbose_name='Книги добавленные в избранное'),
        ),
    ]
