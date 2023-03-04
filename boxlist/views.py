from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from project.views import HxOnlyTemplateMixin, HxPageTemplateMixin

from .forms import ItemCreateForm
from .models import Item


class ItemListView(HxPageTemplateMixin, ListView):
    model = Item
    template_name = "boxlist/htmx/list.html"


class ItemListRefreshView(ItemListView, HxOnlyTemplateMixin):
    template_name = "boxlist/htmx/list_refresh.html"


class ItemCreateView(HxOnlyTemplateMixin, CreateView):
    model = Item
    form_class = ItemCreateForm
    template_name = "boxlist/htmx/create.html"

    def form_valid(self, form):
        last = Item.objects.last()
        form.instance.position = last.position + 1
        return super(ItemCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("boxlist:list_refresh")


class ItemDetailView(HxOnlyTemplateMixin, DetailView):
    model = Item
    context_object_name = "item"
    template_name = "boxlist/htmx/detail.html"


class ItemUpdateView(HxOnlyTemplateMixin, UpdateView):
    model = Item
    form_class = ItemCreateForm
    template_name = "boxlist/htmx/update.html"

    def get_success_url(self):
        return reverse("boxlist:detail", kwargs={"pk": self.object.id})


class ItemDeleteView(HxOnlyTemplateMixin, TemplateView):
    template_name = "boxlist/htmx/delete.html"

    def setup(self, request, *args, **kwargs):
        super(ItemDeleteView, self).setup(request, *args, **kwargs)
        item = get_object_or_404(Item, id=self.kwargs["pk"])
        item.delete()
