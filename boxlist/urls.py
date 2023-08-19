from django.urls import path

from .views import (  # noqa
    item_detail,
    item_list_create,
    item_review_update_delete,
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
        "item/sort/",
        item_sort,
        name="sort",
    ),
    path(
        "item/<pk>/",
        item_review_update_delete,
        name="detail",
    ),
    path(
        "item/<pk>/update/",
        item_update,
        name="update",
    ),
]
