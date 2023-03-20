from django.urls import path

from .views import PhaseListView

app_name = "timeline"
urlpatterns = [
    path(
        "",
        PhaseListView.as_view(),
        name="list",
    ),
]
