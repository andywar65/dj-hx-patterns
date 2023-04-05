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


class ItemCreateView(HxOnlyTemplateMixin, CreateView):
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
    template_name = "boxlist/htmx/add_button.html"


class ItemDetailView(HxOnlyTemplateMixin, DetailView):
    model = Item
    context_object_name = "item"
    template_name = "boxlist/htmx/detail.html"

    def dispatch(self, request, *args, **kwargs):
        response = super(ItemDetailView, self).dispatch(request, *args, **kwargs)
        response["HX-Retarget"] = "#item-%(id)s" % {"id": self.object.id}
        return response


class ItemUpdateView(HxOnlyTemplateMixin, UpdateView):
    model = Item
    form_class = ItemCreateForm
    template_name = "boxlist/htmx/update.html"

    def get_success_url(self):
        return reverse("boxlist:detail", kwargs={"pk": self.object.id})

    def dispatch(self, request, *args, **kwargs):
        response = super(ItemUpdateView, self).dispatch(request, *args, **kwargs)
        response["HX-Retarget"] = "#item-%(id)s" % {"id": self.object.id}
        return response


class ItemDeleteView(HxOnlyTemplateMixin, TemplateView):
    template_name = "boxlist/htmx/delete.html"

    def setup(self, request, *args, **kwargs):
        super(ItemDeleteView, self).setup(request, *args, **kwargs)
        item = get_object_or_404(Item, id=self.kwargs["pk"])
        item.move_following_items()
        self.id = item.id
        item.delete()

    def dispatch(self, request, *args, **kwargs):
        response = super(ItemDeleteView, self).dispatch(request, *args, **kwargs)
        response["HX-Retarget"] = "#item-%(id)s" % {"id": self.id}
        return response


class ItemMoveDownView(HxOnlyTemplateMixin, TemplateView):
    template_name = "boxlist/htmx/moving.html"

    def setup(self, request, *args, **kwargs):
        super(ItemMoveDownView, self).setup(request, *args, **kwargs)
        self.object = get_object_or_404(Item, id=self.kwargs["pk"])
        self.object.move_down()


class ItemMoveUpView(HxOnlyTemplateMixin, TemplateView):
    template_name = "boxlist/htmx/moving.html"

    def setup(self, request, *args, **kwargs):
        super(ItemMoveUpView, self).setup(request, *args, **kwargs)
        self.object = get_object_or_404(Item, id=self.kwargs["pk"])
        self.object.move_up()
