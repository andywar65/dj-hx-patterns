# from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView

from project.views import HxOnlyTemplateMixin, HxPageTemplateMixin

from .forms import RowCreateForm
from .models import Row

# ; DetailView,; RedirectView,; TemplateView,; UpdateView,


class RowListView(HxPageTemplateMixin, ListView):
    model = Row
    paginate_by = 10
    template_name = "bulktable/htmx/list.html"


class RowListRefreshView(RowListView, HxOnlyTemplateMixin):
    template_name = "bulktable/htmx/list_refresh.html"


class RowCreateView(HxOnlyTemplateMixin, CreateView):
    model = Row
    form_class = RowCreateForm
    template_name = "bulktable/htmx/create.html"

    def get_success_url(self):
        return reverse("bulktable:list_refresh")
