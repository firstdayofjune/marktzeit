from django.contrib import admin

from . import models


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["id", "street", "street_number", "postal_code", "town"]


@admin.register(models.OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "supermarket",
        "weekday",
        "opening_time",
        "closing_time",
    ]


@admin.register(models.Supermarket)
class SupermarketAdmin(admin.ModelAdmin):
    list_display = ["id", "chain", "name", "address"]


@admin.register(models.SupermarketChain)
class SupermarketChainAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
