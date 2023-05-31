from django.urls import path

from .views import (
    EventEmitterView,
    ItemAddButtonView,
    ItemCreateView,
    ItemDetailView,
    ItemSortView,
    ItemUpdateView,
    item_list,
)

app_name = "boxlist"
urlpatterns = [
    path(
        "",
        item_list,
        name="list",
    ),
    path(
        "item/create/",
        ItemCreateView.as_view(),
        name="create",
    ),
    path(
        "item/add/button/",
        ItemAddButtonView.as_view(),
        name="add_button",
    ),
    path(
        "item/sort/",
        ItemSortView.as_view(),
        name="sort",
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
        "event-emit/",
        EventEmitterView.as_view(),
        name="event_emit",
    ),
]
