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
        return reverse("boxlist:add_button") + "?refresh=true"

    def dispatch(self, request, *args, **kwargs):
        response = super(ItemCreateView, self).dispatch(request, *args, **kwargs)
        response["HX-Retarget"] = "#add-button"
        return response


class ItemAddButtonView(HxOnlyTemplateMixin, TemplateView):
    template_name = "boxlist/htmx/add_button.html"

    def dispatch(self, request, *args, **kwargs):
        response = super(ItemAddButtonView, self).dispatch(request, *args, **kwargs)
        response["HX-Retarget"] = "#add-button"
        if "refresh" in request.GET:
            response["HX-Trigger-After-Swap"] = "refreshList"
        return response


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
        item.delete()


class ItemMoveDownView(HxOnlyTemplateMixin, RedirectView):
    def setup(self, request, *args, **kwargs):
        super(ItemMoveDownView, self).setup(request, *args, **kwargs)
        item = get_object_or_404(Item, id=self.kwargs["pk"])
        item.move_down()

    def get_redirect_url(self, *args, **kwargs):
        return reverse("boxlist:list")


class ItemMoveUpView(HxOnlyTemplateMixin, RedirectView):
    def setup(self, request, *args, **kwargs):
        super(ItemMoveUpView, self).setup(request, *args, **kwargs)
        item = get_object_or_404(Item, id=self.kwargs["pk"])
        item.move_up()

    def get_redirect_url(self, *args, **kwargs):
        return reverse("boxlist:list")
