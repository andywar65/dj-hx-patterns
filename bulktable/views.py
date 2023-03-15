from django.contrib import messages

# from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, TemplateView

from project.views import HxOnlyTemplateMixin, HxPageTemplateMixin

from .forms import RowCreateForm
from .models import Row

# ; DetailView,; RedirectView,; T,; UpdateView,


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

    def form_valid(self, form):
        report = _("Added row with title: ") + form.instance.title
        messages.success(self.request, report)
        return super(RowCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("bulktable:add_button") + "?refresh=true"


class RowAddButtonView(HxOnlyTemplateMixin, TemplateView):
    template_name = "bulktable/htmx/add_button.html"

    def dispatch(self, request, *args, **kwargs):
        response = super(RowAddButtonView, self).dispatch(request, *args, **kwargs)
        if "refresh" in request.GET:
            response["HX-Trigger-After-Swap"] = "refreshList"
        return response
