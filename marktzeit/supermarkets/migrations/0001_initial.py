# Generated by Django 2.2.11 on 2020-03-21 13:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('street', models.CharField(max_length=255)),
                ('street_number', models.CharField(max_length=10)),
                ('postal_code', models.CharField(max_length=10)),
                ('town', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupermarketChain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supermarket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('people_per_slot', models.PositiveIntegerField(help_text='How many people are allowed to book one slot?', verbose_name='people per slot')),
                ('minutes_per_slot', models.PositiveIntegerField(help_text='How long is one slot?', verbose_name='minutes per slot')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supermarkets.Address', verbose_name='address')),
                ('chain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supermarkets.SupermarketChain', verbose_name='chain')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
