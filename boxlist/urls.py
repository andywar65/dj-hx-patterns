from django.urls import path
from django.utils.translation import gettext_lazy as _  # noqa

from .views import BoxListView

app_name = "boxlist"
urlpatterns = [
    path(
        "",
        BoxListView.as_view(),
        name="list",
    ),
]
