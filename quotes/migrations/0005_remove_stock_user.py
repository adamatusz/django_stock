# Generated by Django 4.0.6 on 2022-07-06 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_stock_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='user',
        ),
    ]
