from django.views.generic import TemplateView

from project.views import HxPageTemplateMixin


class BoxListView(HxPageTemplateMixin, TemplateView):
    template_name = "boxlist/htmx/list.html"
