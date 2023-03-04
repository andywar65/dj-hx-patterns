from django.urls import path
from django.utils.translation import gettext_lazy as _  # noqa

from .views import (
    ItemCreateView,
    ItemDeleteView,
    ItemDetailView,
    ItemListRefreshView,
    ItemListView,
    ItemUpdateView,
)

app_name = "boxlist"
urlpatterns = [
    path(
        "",
        ItemListView.as_view(),
        name="list",
    ),
    path(
        "refresh/",
        ItemListRefreshView.as_view(),
        name="list_refresh",
    ),
    path(
        "item/create/",
        ItemCreateView.as_view(),
        name="create",
    ),
    path(
        "item/<pk>/",
        ItemDetailView.as_view(),
        name="detail",
    ),
    path(
        "item/<pk>/update/",
        ItemUpdateView.as_view(),
        name="update",
    ),
    path(
        "item/<pk>/delete/",
        ItemDeleteView.as_view(),
        name="delete",
    ),
]
