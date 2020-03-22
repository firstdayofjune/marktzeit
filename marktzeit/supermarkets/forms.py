from datetime import time

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from marktzeit.supermarkets.models import OpeningHours


class SupermarketCSVUploadForm(forms.Form):
    """Form for uploading a CSV file in the format provided by
    filialstandorte.de and creating/updating supermarket objects from it.
    """

    csv_file = forms.FileField()
    default_working_days = forms.MultipleChoiceField(
        label=_("Default working days"),
        choices=OpeningHours.WEEKDAYS,
        initial=[d for d in range(1, 7)],  # Mon - Sat
        required=False,
        help_text=_(
            "All the imported supermarkets will have opening hours set for"
            " these days of the week. Not choosing any days will not add any"
            " opening hours for the imported supermarkets"
        ),
    )
    default_opening_time = forms.ChoiceField(
        label=_("Default opening time"),
        initial=time(8, 0),
        choices=OpeningHours.TIMES,
        help_text=_(
            "The opening hours opening time for all of the selected days"
        ),
    )
    default_closing_time = forms.ChoiceField(
        label=_("Default closing time"),
        initial=time(20, 0),
        choices=OpeningHours.TIMES,
        help_text=_(
            "The opening hours closing time for all of the selected days"
        ),
    )
    default_people_per_slot = forms.IntegerField(
        label=_("Default people per slot"),
        min_value=1,
        initial=10,
        help_text=_(
            "All the supermarkets will be created with slots allowing this"
            " many people at a time"
        ),
    )
    default_minutes_per_slot = forms.IntegerField(
        label=_("Default minutes per slot"),
        min_value=1,
        initial=10,
        help_text=_(
            "All the supermarkets will be created with slots that last"
            " this many minutes"
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            # validation already failed
            return cleaned_data

        if (
            cleaned_data["default_working_days"]
            and cleaned_data["default_opening_time"]
            >= cleaned_data["default_closing_time"]
        ):
            raise ValidationError(
                {
                    "default_opening_time": _(
                        "Opening time must be before closing time."
                    )
                }
            )
        return cleaned_data
