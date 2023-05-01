from django.http import Http404
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
