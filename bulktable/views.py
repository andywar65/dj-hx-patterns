from django.contrib import messages

# from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, FormView, ListView, TemplateView

from project.views import HxOnlyTemplateMixin, HxPageTemplateMixin

from .forms import RowCreateForm, RowUpdateForm
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


class RowUpdateView(HxOnlyTemplateMixin, FormView):
    form_class = RowUpdateForm
    template_name = "bulktable/htmx/update.html"

    def form_valid(self, form):
        if "ids" in self.request.POST:
            updated = 0
            id_list = self.request.POST.getlist("ids")
            title = form.cleaned_data["title"]
            color = form.cleaned_data["color"]
            for row in Row.objects.filter(id__in=id_list):
                if title:
                    row.title = title
                if color:
                    row.color = color
                if title or color:
                    row.save()
                    updated += 1
            messages.success(
                self.request,
                _("Updated %(updated)s row(s).") % {"updated": str(updated)},
            )
        return super(RowUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("bulktable:update_button") + "?refresh=true"


class RowDeleteView(HxOnlyTemplateMixin, TemplateView):
    template_name = "bulktable/htmx/update_button.html"

    def dispatch(self, request, *args, **kwargs):
        if "ids" in self.request.GET:
            deleted = 0
            id_list = self.request.GET.getlist("ids")
            for row in Row.objects.filter(id__in=id_list):
                row.delete()
                deleted += 1
            messages.error(
                self.request,
                _("Deleted %(deleted)s row(s).") % {"deleted": str(deleted)},
            )
        response = super(RowDeleteView, self).dispatch(request, *args, **kwargs)
        response["HX-Trigger-After-Swap"] = "refreshList"
        return response


class RowUpdateButtonView(HxOnlyTemplateMixin, TemplateView):
    template_name = "bulktable/htmx/update_button.html"

    def dispatch(self, request, *args, **kwargs):
        response = super(RowUpdateButtonView, self).dispatch(request, *args, **kwargs)
        if "refresh" in request.GET:
            response["HX-Trigger-After-Swap"] = "refreshList"
        return response
