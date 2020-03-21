from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


@admin.register(models.Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ["id", "time_range_display"]

    def time_range_display(self, slot):
        return (
            f"{slot.time_range.lower:%Y-%m-%d %H:%M}"
            f" - {slot.time_range.upper:%Y-%m-%d %H:%M}"
        )
    time_range_display.short_description = _("time range")
    time_range_display.admin_order_field = "time_range"
