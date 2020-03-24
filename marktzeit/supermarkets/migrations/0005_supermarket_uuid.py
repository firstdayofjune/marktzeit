# Generated by Django 2.2.11 on 2020-03-22 17:22

from django.db import migrations, models
import uuid


def set_uuids(apps, schema_editor):
    Supermarket = apps.get_model("supermarkets", "Supermarket")
    for supermarket in Supermarket.objects.all():
        supermarket.uuid = uuid.uuid4()
        supermarket.save()


class Migration(migrations.Migration):

    dependencies = [
        ("supermarkets", "0004_auto_20200322_1047"),
    ]

    operations = [
        migrations.AddField(
            model_name="supermarket",
            name="uuid",
            field=models.UUIDField(blank=True, null=True, verbose_name="uuid"),
        ),
        migrations.RunPython(set_uuids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="supermarket",
            name="uuid",
            field=models.UUIDField(unique=True, verbose_name="uuid"),
        ),
    ]
