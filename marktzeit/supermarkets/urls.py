from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "supermarkets"
urlpatterns = [
    path(
        "",
        view=TemplateView.as_view(
            template_name="supermarkets/markt_search.html"
        ),
        name="markt-search",
    ),
    path(
        "markt-detail/",
        view=TemplateView.as_view(
            template_name="supermarkets/markt_detail.html"
        ),
        name="markt-detail",
    ),
    path(
        "markt-list/",
        view=TemplateView.as_view(
            template_name="supermarkets/markt_list.html"
        ),
        name="markt-list",
    ),
    path("search/", view=views.search, name="redirect"),
]