from django.urls import path

from .views import (  # noqa
    add_button,
    item_create,
    item_detail,
    item_list,
    item_list_create,
    item_sort,
    item_update,
)

app_name = "boxlist"
urlpatterns = [
    path(
        "",
        item_list_create,
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
        item_update,
        name="update",
    ),
]
