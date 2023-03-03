from django.views.generic import TemplateView


class BoxListView(TemplateView):
    template_name = "boxlist/htmx/list.html"
