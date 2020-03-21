from django.conf import settings
from django.contrib.postgres.fields import DateTimeRangeField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from marktzeit.supermarkets.models import Supermarket


class Slot(TimeStampedModel):
    """Represents a supermarket time slot that can be booked by a user"""

    supermarket = models.ForeignKey(
        Supermarket, verbose_name=_("supermarket"), on_delete=models.CASCADE
    )
    time_range = DateTimeRangeField(
        verbose_name=_("time range"),
        help_text=_("The time range during which this slot is active"),
    )
    booked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("booked by"),
        help_text=_("The people that booked this time slot"),
    )
