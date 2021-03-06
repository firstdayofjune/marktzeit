# Generated by Django 2.2.11 on 2020-03-21 16:26

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('supermarkets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('weekday', models.PositiveSmallIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], help_text='The day of the week on which these opening times are applicable', verbose_name='weekday')),
                ('opening_time', models.TimeField(choices=[(datetime.time(0, 0), '00:00'), (datetime.time(0, 30), '00:30'), (datetime.time(1, 0), '01:00'), (datetime.time(1, 30), '01:30'), (datetime.time(2, 0), '02:00'), (datetime.time(2, 30), '02:30'), (datetime.time(3, 0), '03:00'), (datetime.time(3, 30), '03:30'), (datetime.time(4, 0), '04:00'), (datetime.time(4, 30), '04:30'), (datetime.time(5, 0), '05:00'), (datetime.time(5, 30), '05:30'), (datetime.time(6, 0), '06:00'), (datetime.time(6, 30), '06:30'), (datetime.time(7, 0), '07:00'), (datetime.time(7, 30), '07:30'), (datetime.time(8, 0), '08:00'), (datetime.time(8, 30), '08:30'), (datetime.time(9, 0), '09:00'), (datetime.time(9, 30), '09:30'), (datetime.time(10, 0), '10:00'), (datetime.time(10, 30), '10:30'), (datetime.time(11, 0), '11:00'), (datetime.time(11, 30), '11:30'), (datetime.time(12, 0), '12:00'), (datetime.time(12, 30), '12:30'), (datetime.time(13, 0), '13:00'), (datetime.time(13, 30), '13:30'), (datetime.time(14, 0), '14:00'), (datetime.time(14, 30), '14:30'), (datetime.time(15, 0), '15:00'), (datetime.time(15, 30), '15:30'), (datetime.time(16, 0), '16:00'), (datetime.time(16, 30), '16:30'), (datetime.time(17, 0), '17:00'), (datetime.time(17, 30), '17:30'), (datetime.time(18, 0), '18:00'), (datetime.time(18, 30), '18:30'), (datetime.time(19, 0), '19:00'), (datetime.time(19, 30), '19:30'), (datetime.time(20, 0), '20:00'), (datetime.time(20, 30), '20:30'), (datetime.time(21, 0), '21:00'), (datetime.time(21, 30), '21:30'), (datetime.time(22, 0), '22:00'), (datetime.time(22, 30), '22:30'), (datetime.time(23, 0), '23:00'), (datetime.time(23, 30), '23:30'), (datetime.time(23, 59, 59, 999999), 'midnight')], default=datetime.time(8, 0), help_text='The time at which the supermarket opens.', verbose_name='opening time')),
                ('closing_time', models.TimeField(choices=[(datetime.time(0, 0), '00:00'), (datetime.time(0, 30), '00:30'), (datetime.time(1, 0), '01:00'), (datetime.time(1, 30), '01:30'), (datetime.time(2, 0), '02:00'), (datetime.time(2, 30), '02:30'), (datetime.time(3, 0), '03:00'), (datetime.time(3, 30), '03:30'), (datetime.time(4, 0), '04:00'), (datetime.time(4, 30), '04:30'), (datetime.time(5, 0), '05:00'), (datetime.time(5, 30), '05:30'), (datetime.time(6, 0), '06:00'), (datetime.time(6, 30), '06:30'), (datetime.time(7, 0), '07:00'), (datetime.time(7, 30), '07:30'), (datetime.time(8, 0), '08:00'), (datetime.time(8, 30), '08:30'), (datetime.time(9, 0), '09:00'), (datetime.time(9, 30), '09:30'), (datetime.time(10, 0), '10:00'), (datetime.time(10, 30), '10:30'), (datetime.time(11, 0), '11:00'), (datetime.time(11, 30), '11:30'), (datetime.time(12, 0), '12:00'), (datetime.time(12, 30), '12:30'), (datetime.time(13, 0), '13:00'), (datetime.time(13, 30), '13:30'), (datetime.time(14, 0), '14:00'), (datetime.time(14, 30), '14:30'), (datetime.time(15, 0), '15:00'), (datetime.time(15, 30), '15:30'), (datetime.time(16, 0), '16:00'), (datetime.time(16, 30), '16:30'), (datetime.time(17, 0), '17:00'), (datetime.time(17, 30), '17:30'), (datetime.time(18, 0), '18:00'), (datetime.time(18, 30), '18:30'), (datetime.time(19, 0), '19:00'), (datetime.time(19, 30), '19:30'), (datetime.time(20, 0), '20:00'), (datetime.time(20, 30), '20:30'), (datetime.time(21, 0), '21:00'), (datetime.time(21, 30), '21:30'), (datetime.time(22, 0), '22:00'), (datetime.time(22, 30), '22:30'), (datetime.time(23, 0), '23:00'), (datetime.time(23, 30), '23:30'), (datetime.time(23, 59, 59, 999999), 'midnight')], default=datetime.time(20, 0), help_text='The time at which the supermarket closes.', verbose_name='closing time')),
                ('supermarket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supermarkets.Supermarket', verbose_name='supermarket')),
            ],
            options={
                'abstract': False,
                'ordering': ["supermarket", "weekday", "opening_time", "closing_time"],
                'verbose_name': 'Opening hours',
                'verbose_name_plural': 'Opening hours',
            },
        ),
    ]
