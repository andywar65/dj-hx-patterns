from django.urls import path
from django.utils.translation import gettext_lazy as _  # noqa

from .views import CategoryListView

app_name = "hierarchy"
urlpatterns = [
    path(
        "",
        CategoryListView.as_view(),
        name="list",
    ),
]
