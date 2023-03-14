from django.shortcuts import render  # noqa
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

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


class CategoryDetailView(HxOnlyTemplateMixin, DetailView):
    model = Category
    context_object_name = "category"
    template_name = "hierarchy/htmx/detail.html"


class CategoryUpdateView(HxOnlyTemplateMixin, UpdateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = "hierarchy/htmx/update.html"

    def get_success_url(self):
        return reverse("hierarchy:detail", kwargs={"pk": self.object.id})

    def dispatch(self, request, *args, **kwargs):
        # TODO has to work if parent is updated
        response = super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)
        # response["HX-Trigger-After-Swap"] = "refreshList"
        return response
