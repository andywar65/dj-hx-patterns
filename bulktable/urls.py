from django.urls import path

from .views import (
    RowAddButtonView,
    RowCreateView,
    RowListRefreshView,
    RowListView,
    RowUpdateButtonView,
    RowUpdateView,
)

# ; ; RowDeleteView,; RowDetailView,; RowUpdateView,

app_name = "bulktable"
urlpatterns = [
    path(
        "",
        RowListView.as_view(),
        name="list",
    ),
    path(
        "refresh/",
        RowListRefreshView.as_view(),
        name="list_refresh",
    ),
    path(
        "row/create/",
        RowCreateView.as_view(),
        name="create",
    ),
    path(
        "row/add/button/",
        RowAddButtonView.as_view(),
        name="add_button",
    ),
    path(
        "row/update/",
        RowUpdateView.as_view(),
        name="update",
    ),
    path(
        "row/update/button/",
        RowUpdateButtonView.as_view(),
        name="update_button",
    ),
]
