from django.urls import reverse
from django.views.generic import CreateView, ListView  # , TemplateView

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

    def get_success_url(self):
        return reverse("boxlist:list_refresh")
