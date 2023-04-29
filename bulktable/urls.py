from django.urls import path

from .views import (
    EventEmitterView,
    RowControllersView,
    RowCreateView,
    RowDeleteView,
    RowDetailView,
    RowListView,
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
