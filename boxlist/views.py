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
    """Rendered in #content"""

    model = Item
    template_name = "boxlist/htmx/list.html"


class ItemCreateView(HxOnlyTemplateMixin, CreateView):
    """Rendered in #add-button, on success targets #content"""

    model = Item
    form_class = ItemCreateForm
    template_name = "boxlist/htmx/create.html"

    def form_valid(self, form):
        last = Item.objects.last()
        form.instance.position = last.position + 1
        return super(ItemCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("boxlist:list")


class ItemAddButtonView(HxOnlyTemplateMixin, TemplateView):
    """Rendered in #add-button when create is dismissed"""

    template_name = "boxlist/htmx/add_button.html"


class ItemUpdateView(HxOnlyTemplateMixin, UpdateView):
    """Rendered in #item-{{ item.id }}"""

    model = Item
    form_class = ItemCreateForm
    template_name = "boxlist/htmx/update.html"

    def get_success_url(self):
        return reverse("boxlist:detail", kwargs={"pk": self.object.id})


class ItemDetailView(HxOnlyTemplateMixin, DetailView):
    """Rendered in #item-{{ item.id }} when update is performed or dismissed"""

    model = Item
    context_object_name = "item"
    template_name = "boxlist/htmx/detail.html"


class ItemDeleteView(HxOnlyTemplateMixin, TemplateView):
    """Rendered in #item-{{ item.id }}, then triggers list in #content"""

    template_name = "boxlist/htmx/delete.html"

    def setup(self, request, *args, **kwargs):
        super(ItemDeleteView, self).setup(request, *args, **kwargs)
        item = get_object_or_404(Item, id=self.kwargs["pk"])
        item.move_following_items()
        item.delete()


class ItemMoveDownView(HxOnlyTemplateMixin, TemplateView):
    """Rendered in #item-{{ item.id }}, then triggers list in #content"""

    template_name = "boxlist/htmx/moving.html"

    def setup(self, request, *args, **kwargs):
        super(ItemMoveDownView, self).setup(request, *args, **kwargs)
        item = get_object_or_404(Item, id=self.kwargs["pk"])
        item.move_down()


class ItemMoveUpView(HxOnlyTemplateMixin, TemplateView):
    """Rendered in #item-{{ item.id }}, then triggers list in #content"""

    template_name = "boxlist/htmx/moving.html"

    def setup(self, request, *args, **kwargs):
        super(ItemMoveUpView, self).setup(request, *args, **kwargs)
        item = get_object_or_404(Item, id=self.kwargs["pk"])
        item.move_up()
