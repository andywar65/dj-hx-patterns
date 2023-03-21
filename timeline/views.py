from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, TemplateView

from project.views import HxOnlyTemplateMixin, HxPageTemplateMixin

from .forms import PhaseCreateForm
from .models import Phase, get_position_by_parent


class PhaseListView(HxPageTemplateMixin, ListView):
    model = Phase
    template_name = "timeline/htmx/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PhaseListView, self).get_context_data()
        context["object_list"] = context["object_list"].with_tree_fields()
        return context


class PhaseCreateView(HxOnlyTemplateMixin, CreateView):
    model = Phase
    form_class = PhaseCreateForm
    template_name = "timeline/htmx/create.html"

    def form_valid(self, form):
        form.instance.position = get_position_by_parent(form.instance.parent)
        report = _("Added phase with title: ") + form.instance.title
        messages.success(self.request, report)
        return super(PhaseCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("timeline:add_button") + "?refresh=true"


class PhaseAddButtonView(HxOnlyTemplateMixin, TemplateView):
    template_name = "timeline/htmx/add_button.html"

    def dispatch(self, request, *args, **kwargs):
        response = super(PhaseAddButtonView, self).dispatch(request, *args, **kwargs)
        if "refresh" in request.GET:
            response["HX-Trigger-After-Swap"] = "refreshList"
        return response
