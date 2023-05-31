import json

from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView, FormView, RedirectView, TemplateView

from project.views import HxOnlyTemplateMixin

from .forms import ItemCreateForm, ItemUpdateForm
from .models import Item, intercalate_siblings, move_down_siblings


def item_list(request):
    """Rendered in #content"""

    template_name = "boxlist/htmx/list.html"
    if not request.htmx:
        template_name = template_name.replace("htmx/", "")
    context = {"object_list": Item.objects.all()}
    return TemplateResponse(request, template_name, context)


class ItemCreateView(HxOnlyTemplateMixin, FormView):
    """Rendered in #add-button, on success targets #content"""

    form_class = ItemCreateForm
    template_name = "boxlist/htmx/create.html"

    def get_initial(self):
        initial = super().get_initial()
        last = Item.objects.last()
        initial["target"] = last.id
        return initial

    def form_valid(self, form):
        position = 1
        if form.cleaned_data["target"]:
            position = form.cleaned_data["target"].position + 1
        move_down_siblings(position)
        object = Item()
        object.title = form.cleaned_data["title"]
        object.position = position
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("boxlist:list")


class ItemAddButtonView(HxOnlyTemplateMixin, TemplateView):
    """Rendered in #add-button when create is dismissed"""

    template_name = "boxlist/htmx/add_button.html"


class ItemSortView(RedirectView):
    """Updates POSTed positions of items and redirects
    to the EventemitterView"""

    def get_redirect_url(self, *args, **kwargs):
        if not self.request.htmx:
            raise Http404("Request without HTMX headers")
        events = []
        if "item" in self.request.POST:
            i = 1
            id_list = self.request.POST.getlist("item")
            for id in id_list:
                item = get_object_or_404(Item, id=id)
                if not item.position == i:
                    item.position = i
                    item.save()
                    events.append("event=refreshItem" + str(item.id))
                i += 1
        return reverse("boxlist:event_emit") + "?%(string)s" % {
            "string": "&".join(events)
        }


class ItemUpdateView(HxOnlyTemplateMixin, FormView):
    """Rendered in #item-{{ item.id }}, on success swaps none
    and refreshes #item-{{ item.id }} or #content if position changed.
    If DELETE method, swaps in #item-{{ item.id }}"""

    form_class = ItemUpdateForm
    template_name = "boxlist/htmx/update.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object = get_object_or_404(Item, id=self.kwargs["pk"])
        self.original_position = self.object.position

    def get_initial(self):
        initial = super().get_initial()
        initial["title"] = self.object.title
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.object
        return context

    def form_valid(self, form):
        position = self.original_position
        if form.cleaned_data["target"]:
            position = form.cleaned_data["target"].position
        intercalate_siblings(position, self.original_position)
        self.object.title = form.cleaned_data["title"]
        self.object.position = position
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        if not self.object.position == self.original_position:
            return reverse("boxlist:event_emit") + "?event=refreshList"
        return (
            reverse("boxlist:event_emit") + "?event=refreshItem" + str(self.object.id)
        )

    def delete(self, request, **kwargs):
        item = get_object_or_404(Item, id=kwargs["pk"])
        item.move_following_items()
        item.delete()
        return render(request, "boxlist/htmx/delete.html")


class ItemDetailView(HxOnlyTemplateMixin, DetailView):
    """Rendered in #item-{{ item.id }} when update is dismissed or successful"""

    model = Item
    template_name = "boxlist/htmx/detail.html"


class EventEmitterView(HxOnlyTemplateMixin, TemplateView):
    """This view emits an event: gets list of event paramenters
    and dispatches event dictinary. Renders none template as
    swapping is null"""

    template_name = "boxlist/htmx/none.html"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if "event" in request.GET:
            event_dict = {}
            events = request.GET.getlist("event")
            for e in events:
                event_dict[e] = "true"
            response["HX-Trigger"] = json.dumps(event_dict)
        return response
