import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from model_utils.models import TimeStampedModel


def _get_time_choices():
    """To make it easier to pick the opening and closing times, we pre-generate
    a list of times in 30 minute intervals.
    """
    times = []
    for hour in range(24):
        for minutes in (0, 30):
            _time = datetime.time(hour, minutes)
            times.append((_time, _time.strftime("%H:%M")))
    times.append((datetime.time.max, _("midnight")))  # special case
    return times


class Address(TimeStampedModel):
    """Represents a physical address"""

    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    town = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self):
        return f"{self.street} {self.street_number}, {self.postal_code} {self.town}"


class SupermarketChain(TimeStampedModel):
    """Represents the entity that owns multiple supermarkets"""

    name = models.CharField(max_length=255, verbose_name=_("name"))

    class Meta:
        verbose_name = _("supermarket chain")
        verbose_name_plural = _("supermarket chains")

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

    class Meta:
        verbose_name = _("supermarket")
        verbose_name_plural = _("supermarkets")

    def __str__(self):
        return f"{self.chain} - {self.name}"


class OpeningHours(TimeStampedModel):
    """A single set of opening and closing times for a specific day of the week
    for a supermarket.

    A supermarket can have multiple opening hours for a specific weekday, as
    long as they don't overlap.

    NOTE: if a supermarket is open from Tuesday 14:00 to Wednesday 02:00, two
    separate OpeningHours would need to be made:
    Tuesday 14:00 to midnight and Wednesday 00:00 to 02:00.
    """

    # isoweekday
    WEEKDAYS = [
        (1, _("Monday")),
        (2, _("Tuesday")),
        (3, _("Wednesday")),
        (4, _("Thursday")),
        (5, _("Friday")),
        (6, _("Saturday")),
        (7, _("Sunday")),
    ]

    supermarket = models.ForeignKey(
        Supermarket, verbose_name=_("supermarket"), on_delete=models.CASCADE
    )
    weekday = models.PositiveSmallIntegerField(
        choices=WEEKDAYS,
        verbose_name=_("weekday"),
        help_text=_(
            "The day of the week on which these opening times are applicable"
        ),
    )
    opening_time = models.TimeField(
        choices=_get_time_choices(),
        default=datetime.time(8, 0),
        verbose_name=_("opening time"),
        help_text=_("The time at which the supermarket opens."),
    )
    closing_time = models.TimeField(
        choices=_get_time_choices(),
        default=datetime.time(18, 0),
        verbose_name=_("closing time"),
        help_text=_("The time at which the supermarket closes."),
    )

    class Meta:
        verbose_name = verbose_name_plural = _("opening hours")
        ordering = ["supermarket", "weekday", "opening_time", "closing_time"]

    def __str__(self):
        return ugettext(
            f"{self.supermarket} - {self.get_weekday_display()}"
            f" - {self.opening_time}-{self.closing_time}"
        )

    def clean(self):
        """Ensure the times don't overlap"""
        if not (self.opening_time and self.closing_time):
            # validation already failed
            return

        if self.opening_time >= self.closing_time:
            raise ValidationError(
                {
                    "opening_time": _(
                        "Opening time must be before closing time."
                    )
                }
            )

        if not (self.weekday and self.supermarket):
            # validation already failed
            return

        qs = OpeningHours.objects.filter(
            supermarket=self.supermarket,
            weekday=self.weekday,
            # (open1 < close2) and (open2 < close1)
            opening_time__lt=self.closing_time,
            closing_time__gt=self.opening_time,
        )
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError(
                _(
                    "These opening hours cannot overlap with other opening"
                    " hours for the same day and for the same supermarket: {}"
                ).format(qs.first())
            )
