# Generated by Django 2.2.11 on 2020-03-21 19:48

from django.db import migrations
from psycopg2.extras import DateTimeTZRange


def migrate_times_fwd(app, schema_editor):
    Slot = app.get_model("slots", "Slot")
    for slot in Slot.objects.all():
        slot.start_time = slot.time_range.lower
        slot.end_time = slot.time_range.upper
        slot.save()


def migrate_times_rev(app, schema_editor):
    Slot = app.get_model("slots", "Slot")
    for slot in Slot.objects.all():
        slot.time_range = DateTimeTZRange(slot.start_time, slot.end_time)
        slot.save()


class Migration(migrations.Migration):

    dependencies = [
        ("slots", "0003_auto_20200321_1940"),
    ]

    operations = [
        migrations.RunPython(migrate_times_fwd, migrate_times_rev),
    ]
