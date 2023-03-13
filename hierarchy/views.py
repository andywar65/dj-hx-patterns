from django.shortcuts import render  # noqa
from django.views.generic import ListView

from project.views import HxPageTemplateMixin

from .models import Category


class CategoryListView(HxPageTemplateMixin, ListView):
    model = Category
    template_name = "hierarchy/htmx/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        context["object_list"] = context["object_list"].with_tree_fields()
        return context
