# from django.shortcuts import get_object_or_404
# from django.urls import reverse
from django.views.generic import ListView

from project.views import HxOnlyTemplateMixin, HxPageTemplateMixin

# from .forms import RowCreateForm
from .models import Row

# CreateView,; DetailView,; RedirectView,; TemplateView,; UpdateView,


class RowListView(HxPageTemplateMixin, ListView):
    model = Row
    paginate_by = 10
    template_name = "bulktable/htmx/list.html"


class RowListRefreshView(RowListView, HxOnlyTemplateMixin):
    template_name = "bulktable/htmx/list_refresh.html"
