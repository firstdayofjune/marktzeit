from django.contrib import admin

from . import models


@admin.register(
    models.Address,
    models.OpeningHours,
    models.Supermarket,
    models.SupermarketChain,
)
class SupermarketAdmin(admin.ModelAdmin):  # TODO
    pass
