# Generated by Django 2.2.11 on 2020-03-21 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supermarkets', '0002_openinghours'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'address', 'verbose_name_plural': 'addresses'},
        ),
        migrations.AlterModelOptions(
            name='openinghours',
            options={'ordering': ['supermarket', 'weekday', 'opening_time', 'closing_time'], 'verbose_name': 'opening hours', 'verbose_name_plural': 'opening hours'},
        ),
        migrations.AlterModelOptions(
            name='supermarket',
            options={'verbose_name': 'supermarket', 'verbose_name_plural': 'supermarkets'},
        ),
        migrations.AlterModelOptions(
            name='supermarketchain',
            options={'verbose_name': 'supermarket chain', 'verbose_name_plural': 'supermarket chains'},
        ),
    ]
