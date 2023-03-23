from django.http import Http404
from django.utils.timezone import now
from django.views.generic import TemplateView


class HxPageTemplateMixin:
    """Switches template depending on request.htmx"""

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        return [self.template_name]


class HxOnlyTemplateMixin:
    """Restricts view to HTMX requests"""

    def get_template_names(self):
        if not self.request.htmx:
            raise Http404("Request without HTMX headers")
        return [self.template_name]


class BaseTemplateView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data()
        context["year"] = now().year
        context["month"] = 1
        if now().month > 6:
            context["month"] = 7
        return context
