from django.views.generic import ListView

from project.views import HxOnlyTemplateMixin, HxPageTemplateMixin  # noqa

# from .forms import PhaseCreateForm
from .models import Phase


class PhaseListView(HxPageTemplateMixin, ListView):
    model = Phase
    template_name = "timeline/htmx/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PhaseListView, self).get_context_data()
        context["object_list"] = context["object_list"].with_tree_fields()
        return context
