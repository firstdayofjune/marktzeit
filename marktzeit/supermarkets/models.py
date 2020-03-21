from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Address(TimeStampedModel):
    """Represents a physical address"""

    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    town = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.street} {self.street_number}, {self.postal_code} {self.town}"


class SupermarketChain(TimeStampedModel):
    """Represents the entity that owns multiple supermarkets"""

    name = models.CharField(max_length=255, verbose_name=_("name"))

    def __str__(self):
        return self.name


class Supermarket(TimeStampedModel):
    """Represents a supermarket where users can book slots to visit"""

    name = models.CharField(max_length=255, verbose_name=_("name"))
    chain = models.ForeignKey(
        SupermarketChain, verbose_name=_("chain"), on_delete=models.CASCADE
    )
    address = models.ForeignKey(
        Address, verbose_name=_("address"), on_delete=models.CASCADE
    )
    people_per_slot = models.PositiveIntegerField(
        verbose_name=_("people per slot"),
        help_text=_("How many people are allowed to book one slot?"),
    )
    minutes_per_slot = models.PositiveIntegerField(
        verbose_name=_("minutes per slot"),
        help_text=_("How long is one slot?"),
    )
    # opening_hours  # TODO

    def __str__(self):
        return f"{self.chain} - {self.name}"
