from django.contrib import admin
from django.urls import path

from . import models, views


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

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(
            1,
            path(
                "upload/",
                views.CSVUploadView.as_view(),
                name="supermarkets_supermarket_upload",
            ),
        )
        return urls


@admin.register(models.SupermarketChain)
class SupermarketChainAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
