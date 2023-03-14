from django.shortcuts import render  # noqa
from django.urls import reverse
from django.views.generic import CreateView, ListView, TemplateView

from project.views import HxOnlyTemplateMixin, HxPageTemplateMixin

from .forms import CategoryCreateForm
from .models import Category, get_position_by_parent


class CategoryListView(HxPageTemplateMixin, ListView):
    model = Category
    template_name = "hierarchy/htmx/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        context["object_list"] = context["object_list"].with_tree_fields()
        return context


class CategoryListRefreshView(CategoryListView, HxOnlyTemplateMixin):
    template_name = "hierarchy/htmx/list_refresh.html"


class CategoryCreateView(HxOnlyTemplateMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = "hierarchy/htmx/create.html"

    def form_valid(self, form):
        form.instance.position = get_position_by_parent(form.instance.parent)
        return super(CategoryCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("hierarchy:list_refresh")


class CategoryAddButtonView(HxOnlyTemplateMixin, TemplateView):
    template_name = "hierarchy/htmx/add_button.html"
