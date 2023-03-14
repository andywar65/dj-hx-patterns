from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
)

from project.views import HxOnlyTemplateMixin, HxPageTemplateMixin

from .forms import CategoryCreateForm
from .models import Category, get_position_by_parent, move_younger_siblings


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

    def dispatch(self, request, *args, **kwargs):
        response = super(CategoryDetailView, self).dispatch(request, *args, **kwargs)
        if "refresh" in request.GET:
            response["HX-Trigger-After-Swap"] = "refreshList"
        return response


class CategoryUpdateView(HxOnlyTemplateMixin, UpdateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = "hierarchy/htmx/update.html"

    def setup(self, request, *args, **kwargs):
        super(CategoryUpdateView, self).setup(request, *args, **kwargs)
        self.original_parent = None

    def get_object(self, queryset=None):
        obj = super(CategoryUpdateView, self).get_object(queryset=None)
        self.original_parent = obj.parent
        return obj

    def form_valid(self, form):
        if not self.original_parent == form.instance.parent:
            move_younger_siblings(self.original_parent, form.instance.position)
            form.instance.position = get_position_by_parent(form.instance.parent)
        return super(CategoryUpdateView, self).form_valid(form)

    def get_success_url(self):
        if not self.original_parent == self.object.parent:
            return (
                reverse("hierarchy:detail", kwargs={"pk": self.object.id})
                + "?refresh=true"
            )
        return reverse("hierarchy:detail", kwargs={"pk": self.object.id})


class CategoryDeleteView(HxOnlyTemplateMixin, TemplateView):
    template_name = "hierarchy/htmx/delete.html"

    def setup(self, request, *args, **kwargs):
        super(CategoryDeleteView, self).setup(request, *args, **kwargs)
        category = get_object_or_404(Category, id=self.kwargs["pk"])
        move_younger_siblings(category.parent, category.position)
        category.delete()


class CategoryMoveDownView(HxOnlyTemplateMixin, RedirectView):
    def setup(self, request, *args, **kwargs):
        super(CategoryMoveDownView, self).setup(request, *args, **kwargs)
        category = get_object_or_404(Category, id=self.kwargs["pk"])
        category.move_down()

    def get_redirect_url(self, *args, **kwargs):
        return reverse("hierarchy:list_refresh")


class CategoryMoveUpView(HxOnlyTemplateMixin, RedirectView):
    def setup(self, request, *args, **kwargs):
        super(CategoryMoveUpView, self).setup(request, *args, **kwargs)
        category = get_object_or_404(Category, id=self.kwargs["pk"])
        category.move_up()

    def get_redirect_url(self, *args, **kwargs):
        return reverse("hierarchy:list_refresh")
