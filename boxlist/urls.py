from django.urls import path
from django.utils.translation import gettext_lazy as _  # noqa

from .views import ItemCreateView, ItemListRefreshView, ItemListView

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
]
