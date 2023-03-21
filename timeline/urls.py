from django.urls import path

from .views import PhaseAddButtonView, PhaseCreateView, PhaseListView

app_name = "timeline"
urlpatterns = [
    path(
        "",
        PhaseListView.as_view(),
        name="list",
    ),
    path(
        "phase/create/",
        PhaseCreateView.as_view(),
        name="create",
    ),
    path(
        "phase/add/button/",
        PhaseAddButtonView.as_view(),
        name="add_button",
    ),
]
