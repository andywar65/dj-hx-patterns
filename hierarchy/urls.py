from django.urls import path
from django.utils.translation import gettext_lazy as _  # noqa

from .views import (
    CategoryAddButtonView,
    CategoryCreateView,
    CategoryListRefreshView,
    CategoryListView,
)

app_name = "hierarchy"
urlpatterns = [
    path(
        "",
        CategoryListView.as_view(),
        name="list",
    ),
    path(
        "refresh/",
        CategoryListRefreshView.as_view(),
        name="list_refresh",
    ),
    path(
        "category/create/",
        CategoryCreateView.as_view(),
        name="create",
    ),
    path(
        "category/add/button/",
        CategoryAddButtonView.as_view(),
        name="add_button",
    ),
]
