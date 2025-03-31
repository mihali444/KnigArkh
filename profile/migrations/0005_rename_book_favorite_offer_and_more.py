# Generated by Django 5.1.7 on 2025-03-30 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_bookoffer_user'),
        ('profile', '0004_alter_favorite_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='book',
            new_name='offer',
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'offer')},
        ),
    ]
