import csv
import json
import logging

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.postgres.search import SearchVector
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, FormView, ListView
from rest_framework.reverse import reverse_lazy

from marktzeit.slots.utils import get_slots_for_supermarket
from marktzeit.supermarkets.forms import SupermarketCSVUploadForm
from marktzeit.supermarkets.models import (
    Address,
    OpeningHours,
    Supermarket,
    SupermarketChain,
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


class SupermarketListView(ListView):
    model = Supermarket
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        query_string = self.request.GET.get("q")
        if not query_string or len(query_string) < 4:
            return redirect("supermarkets:markt-search")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        query_string = self.request.GET.get("q")
        return queryset.annotate(
            search=SearchVector(
                "name",
                "chain__name",
                "address__street",
                "address__postal_code",
                "address__suburb",
                "address__town",
                "address__district",
                "address__state",
                config="german",
            )
        ).filter(search=query_string)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(query=self.request.GET.get("q"))
        return context


class SupermarketDetailView(DetailView):
    model = Supermarket
    slug_field = "uuid"
    slug_url_kwarg = "supermarket_uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slots = get_slots_for_supermarket(self.object, timezone.now().date())
        total_slots = len(slots) * self.object.people_per_slot
        booked_slots = sum([slot.booked for slot in slots.values()])
        available_slots = total_slots - booked_slots
        context.update(
            # ensure it will always be chronological
            slots=sorted(slots.items()),
            available_slots=available_slots,
        )
        return context


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
    def _process_row(self, row, cleaned_data):
        """Save the data from a single row"""
        if row["closing"]:
            # this supermarket has closed down
            return 0

        chain = None
        if row["zentrale"] != NULL:
            chain, __ = SupermarketChain.objects.get_or_create(
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

        return 1

    def create_supermarkets(self, reader, cleaned_data):
        """Create the supermarkets from the uploaded data"""
        created = 0
        for idx, row in enumerate(reader):
            try:
                created += self._process_row(row, cleaned_data)
            except Exception as e:
                # intentionally catching broad exception
                # this is so we can log which row failed and why
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    _(
                        "Error occurred on row {}: {!r}. Row content: {}"
                    ).format(idx + 1, e, row),
                )
                break
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
