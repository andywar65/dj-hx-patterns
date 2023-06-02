from django.urls import path

from .views import (
    ItemUpdateView,
    add_button,
    event_emit,
    item_create,
    item_detail,
    item_list,
    item_sort,
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
        item_sort,
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
        event_emit,
        name="event_emit",
    ),
]
