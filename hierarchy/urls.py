from django.urls import path

from .views import (
    CategoryAddButtonView,
    CategoryCreateView,
    CategoryDetailView,
    CategoryListView,
    CategoryMoveDownView,
    CategoryMoveUpView,
    CategoryUpdateView,
    EventEmitterView,
)

app_name = "hierarchy"
urlpatterns = [
    path(
        "",
        CategoryListView.as_view(),
        name="list",
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
    path(
        "category/<pk>/",
        CategoryDetailView.as_view(),
        name="detail",
    ),
    path(
        "category/<pk>/update/",
        CategoryUpdateView.as_view(),
        name="update",
    ),
    path(
        "category/<pk>/move/down/",
        CategoryMoveDownView.as_view(),
        name="move_down",
    ),
    path(
        "category/<pk>/move/up/",
        CategoryMoveUpView.as_view(),
        name="move_up",
    ),
    path(
        "event-emit/",
        EventEmitterView.as_view(),
        name="event_emit",
    ),
]
