from django.urls import path

from .views import (
    EventEmitterView,
    ItemSortView,
    ItemUpdateView,
    add_button,
    item_create,
    item_detail,
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
        item_create,
        name="create",
    ),
    path(
        "item/add/button/",
        add_button,
        name="add_button",
    ),
    path(
        "item/sort/",
        ItemSortView.as_view(),
        name="sort",
    ),
    path(
        "item/<pk>/",
        item_detail,
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
