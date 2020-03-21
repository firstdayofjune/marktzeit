# Generated by Django 2.2.11 on 2020-03-21 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0004_auto_20200321_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='end_time',
            field=models.DateTimeField(help_text='The time at which this slot starts', verbose_name='end time'),
        ),
        migrations.AlterField(
            model_name='slot',
            name='start_time',
            field=models.DateTimeField(help_text='The time at which this slot starts', verbose_name='start time'),
        ),
    ]