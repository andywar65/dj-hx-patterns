from django.urls import path

from .views import (
    ItemAddButtonView,
    ItemCreateView,
    ItemDeleteView,
    ItemDetailView,
    ItemListRefreshView,
    ItemListView,
    ItemMoveDownView,
    ItemMoveUpView,
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
        "item/add/button/",
        ItemAddButtonView.as_view(),
        name="add_button",
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
    path(
        "item/<pk>/move/down/",
        ItemMoveDownView.as_view(),
        name="move_down",
    ),
    path(
        "item/<pk>/move/up/",
        ItemMoveUpView.as_view(),
        name="move_up",
    ),
]
