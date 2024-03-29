import json

from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    RedirectView,
    TemplateView,
)

from project.views import HxOnlyTemplateMixin, HxPageTemplateMixin

from .forms import RowCreateForm, RowUpdateForm
from .models import Row


class RowListView(HxPageTemplateMixin, ListView):
    model = Row
    paginate_by = 10
    template_name = "bulktable/htmx/list.html"


class RowCreateView(HxOnlyTemplateMixin, CreateView):
    model = Row
    form_class = RowCreateForm
    template_name = "bulktable/htmx/create.html"

    def form_valid(self, form):
        report = _("Added row with title: ") + form.instance.title
        messages.success(self.request, report)
        return super(RowCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("bulktable:event_emit") + "?event=refreshList"


class RowDetailView(HxOnlyTemplateMixin, DetailView):
    model = Row
    template_name = "bulktable/htmx/detail.html"


class RowUpdateView(HxOnlyTemplateMixin, FormView):
    form_class = RowCreateForm
    template_name = "bulktable/htmx/update.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.ids = []
        if "ids" in self.request.GET:
            self.ids = request.GET.getlist("ids")
        if "ids" in self.request.POST:
            self.ids = request.POST.getlist("ids")

    def get_form_class(self):
        if len(self.ids) > 1:
            return RowUpdateForm
        return self.form_class

    def get_initial(self):
        initial = super().get_initial()
        if len(self.ids) == 1:
            row = Row.objects.get(id=self.ids[0])
            initial["title"] = row.title
            initial["color"] = row.color
        return initial

    def form_valid(self, form):
        if self.ids:
            updated = 0
            title = None
            if len(self.ids) == 1:
                title = form.cleaned_data["title"]
            color = form.cleaned_data["color"]
            for row in Row.objects.filter(id__in=self.ids):
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
        events = []
        for id in self.ids:
            events.append("event=refreshItem" + str(id))
        return reverse(
            "bulktable:event_emit"
        ) + "?event=refreshControllers&%(string)s" % {"string": "&".join(events)}


class RowDeleteView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # no get_template in redirect view
        if not self.request.htmx:
            raise Http404("Request without HTMX headers")
        # control if we actually have rows and delete them
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
            # control if we deleted all rows in the page
            if len(id_list) == int(self.request.GET["number"]):
                # control if it's not the first page (that may be left empty)
                if int(self.request.GET["page"]) > 1:
                    # go to previous page
                    return (
                        reverse("bulktable:list")
                        + f"?page={int(self.request.GET['page']) - 1}"
                    )
        return reverse("bulktable:list") + f"?page={self.request.GET.get('page')}"


class RowControllersView(HxOnlyTemplateMixin, TemplateView):
    template_name = "bulktable/htmx/controllers.html"


class EventEmitterView(HxOnlyTemplateMixin, TemplateView):
    """This view emits an event"""

    template_name = "bulktable/htmx/none.html"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if "event" in request.GET:
            event_dict = {}
            events = request.GET.getlist("event")
            for e in events:
                event_dict[e] = "true"
            response["HX-Trigger"] = json.dumps(event_dict)
        return response
