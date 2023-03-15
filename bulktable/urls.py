from django.urls import path

from .views import RowCreateView, RowListRefreshView, RowListView

# RowAddButtonView,; ; RowDeleteView,; RowDetailView,; RowUpdateView,

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
]
