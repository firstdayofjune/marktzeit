from django.contrib import admin

from . import models


@admin.register(models.Slot)
class SlotAdmin(admin.ModelAdmin):  # TODO
    pass
