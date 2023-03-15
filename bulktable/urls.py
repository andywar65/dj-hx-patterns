from django.urls import path

from .views import RowListRefreshView, RowListView

# RowAddButtonView,; RowCreateView,; RowDeleteView,; RowDetailView,; RowUpdateView,

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
]
