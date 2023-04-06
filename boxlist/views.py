from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView, TemplateView

from project.views import HxOnlyTemplateMixin, HxPageTemplateMixin

from .forms import ItemCreateForm, ItemUpdateForm
from .models import Item, intercalate_siblings, move_down_siblings


class ItemListView(HxPageTemplateMixin, ListView):
    """Rendered in #content"""

    model = Item
    template_name = "boxlist/htmx/list.html"


class ItemCreateView(HxOnlyTemplateMixin, FormView):
    """Rendered in #add-button, on success targets #content"""

    form_class = ItemCreateForm
    template_name = "boxlist/htmx/create.html"

    def get_initial(self):
        initial = super().get_initial()
        last = Item.objects.last()
        initial["after"] = last.id
        return initial

    def form_valid(self, form):
        position = 1
        if form.cleaned_data["after"]:
            position = form.cleaned_data["after"].position + 1
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


class ItemUpdateView(HxOnlyTemplateMixin, FormView):
    """Rendered in #item-{{ item.id }}, on success targets
    #item-{{ item.id }} and then #content if position changed"""

    # model = Item
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
        if form.cleaned_data["replace"]:
            position = form.cleaned_data["replace"].position
        intercalate_siblings(position, self.original_position)
        self.object.title = form.cleaned_data["title"]
        self.object.position = position
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        if not self.object.position == self.original_position:
            return (
                reverse("boxlist:detail", kwargs={"pk": self.object.id})
                + "?refresh=true"
            )
        return reverse("boxlist:detail", kwargs={"pk": self.object.id})


class ItemDetailView(HxOnlyTemplateMixin, DetailView):
    """Rendered in #item-{{ item.id }} when update is dismissed or successful"""

    model = Item
    context_object_name = "item"
    template_name = "boxlist/htmx/detail.html"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if "refresh" in request.GET:
            response["HX-Trigger-After-Swap"] = "refreshList"
        return response


class ItemDeleteView(HxOnlyTemplateMixin, TemplateView):
    """Rendered in #item-{{ item.id }}, then triggers list in #content"""

    template_name = "boxlist/htmx/delete.html"

    def setup(self, request, *args, **kwargs):
        super(ItemDeleteView, self).setup(request, *args, **kwargs)
        item = get_object_or_404(Item, id=self.kwargs["pk"])
        item.move_following_items()
        item.delete()


class ItemMoveDownView(HxOnlyTemplateMixin, TemplateView):
    """Rendered in #item-{{ item.id }}, then triggers list in #content"""

    template_name = "boxlist/htmx/moving.html"

    def setup(self, request, *args, **kwargs):
        super(ItemMoveDownView, self).setup(request, *args, **kwargs)
        item = get_object_or_404(Item, id=self.kwargs["pk"])
        item.move_down()


class ItemMoveUpView(HxOnlyTemplateMixin, TemplateView):
    """Rendered in #item-{{ item.id }}, then triggers list in #content"""

    template_name = "boxlist/htmx/moving.html"

    def setup(self, request, *args, **kwargs):
        super(ItemMoveUpView, self).setup(request, *args, **kwargs)
        item = get_object_or_404(Item, id=self.kwargs["pk"])
        item.move_up()
