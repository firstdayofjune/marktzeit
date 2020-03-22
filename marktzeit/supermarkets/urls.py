from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "supermarkets"
urlpatterns = [
    path(
        "",
        view=TemplateView.as_view(
            template_name="supermarkets/supermarket_search.html"
        ),
        name="markt-search",
    ),
    path(
        "markt-detail/<uuid:supermarket_uuid>/",
        view=views.SupermarketDetailView.as_view(),
        name="markt-detail",
    ),
    path(
        "markt-list/",
        view=views.SupermarketListView.as_view(),
        name="markt-list",
    ),
    path("search/", view=views.search, name="redirect"),
]
