import csv
import logging
import json

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from rest_framework.reverse import reverse_lazy

from marktzeit.supermarkets.forms import SupermarketCSVUploadForm
from marktzeit.supermarkets.models import (
    Supermarket,
    SupermarketChain,
    Address,
    OpeningHours,
)

logger = logging.getLogger(__name__)

# Constants used in the csv
NULL = "NN"
OTHER = "Sonstiges"


def search(request):
    print(request.GET.get("q"))
    results = {
        "result": [
            {"name": "Mark1", "url": "/markt1"},
            {"name": "Mark2", "url": "/markt2"},
        ]
    }
    results = json.dumps(results)
    return HttpResponse(results)


@method_decorator(
    user_passes_test(lambda user: user.is_superuser), name="dispatch"
)
class CSVUploadView(FormView):
    """View for the CSVUpload form"""

    form_class = SupermarketCSVUploadForm
    success_url = reverse_lazy("admin:supermarkets_supermarket_changelist")
    template_name = "admin/supermarket_upload.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(opts=Supermarket._meta)
        return context

    @transaction.atomic()
    def create_supermarkets(self, reader, cleaned_data):
        """Create the supermarkets from the uploaded data"""
        created = 0
        for row in reader:
            if row["closing"]:
                # this supermarket has closed down
                continue

            chain = None
            if row["zentrale"] != NULL:
                chain, _ = SupermarketChain.objects.get_or_create(
                    name=row["zentrale"]
                )

            address = Address.objects.create(
                street=row["strasse"],
                street_number=row["hausnr"],
                postal_code=row["plz"],
                suburb=row["stadtteil"],
                town=row["ort"],
                district=row["kreis"],
                state=row["bundesland"],
                latitude=row["y"].replace(",", "."),
                longitude=row["x"].replace(",", "."),
            )

            name = (
                row["markttyp"]
                if row["markttyp"] not in [NULL, OTHER]
                else row["inhaber"]
            )

            supermarket = Supermarket(
                chain=chain,
                name=name,
                proprietor=row["inhaber"],
                phone_number=row["fon"],
                fax_number=row["fax"],
                email_address=row["email"],
                website=row["url"],
                address=address,
                people_per_slot=cleaned_data["default_people_per_slot"],
                minutes_per_slot=cleaned_data["default_minutes_per_slot"],
            )
            supermarket.clean()
            supermarket.save()

            for weekday in cleaned_data["default_working_days"]:
                OpeningHours.objects.create(
                    supermarket=supermarket,
                    weekday=weekday,
                    opening_time=cleaned_data["default_opening_time"],
                    closing_time=cleaned_data["default_closing_time"],
                )
            created += 1
        return created

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        file_data = (
            cleaned_data["csv_file"].read().decode("utf-8").splitlines()
        )
        reader = csv.DictReader(
            file_data, delimiter="|", quoting=csv.QUOTE_NONE,
        )

        created = self.create_supermarkets(reader, form.cleaned_data)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("Created {} supermarkets").format(created),
        )

        return super().form_valid(form)
