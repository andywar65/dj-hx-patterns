from django.urls import path

from .views import (
    EventEmitterView,
    RowAddButtonView,
    RowControllersView,
    RowCreateView,
    RowDeleteView,
    RowDetailView,
    RowListView,
    RowUpdateButtonView,
    RowUpdateView,
)

app_name = "bulktable"
urlpatterns = [
    path(
        "",
        RowListView.as_view(),
        name="list",
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
        "row/controllers/",
        RowControllersView.as_view(),
        name="controllers",
    ),
    path(
        "row/update/button/",
        RowUpdateButtonView.as_view(),
        name="update_button",
    ),
    path(
        "row/delete/",
        RowDeleteView.as_view(),
        name="delete",
    ),
    path(
        "row/<pk>/",
        RowDetailView.as_view(),
        name="detail",
    ),
    path(
        "event-emit/",
        EventEmitterView.as_view(),
        name="event_emit",
    ),
]
