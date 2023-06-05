import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .forms import ItemCreateForm, ItemUpdateForm
from .models import Item, intercalate_siblings, move_down_siblings


def check_htmx_request(request):
    """Helper function"""

    if not request.htmx:
        raise Http404("Request without HTMX headers")


def item_list(request):
    """Rendered in #content"""

    template_name = "boxlist/htmx/list.html"
    if not request.htmx:
        template_name = template_name.replace("htmx/", "")
    context = {"object_list": Item.objects.all()}
    return TemplateResponse(request, template_name, context)


def item_create(request):
    """Rendered in #add-button, on success swaps none and triggers
    list refresh"""

    check_htmx_request(request)
    if request.method == "POST":
        form = ItemCreateForm(request.POST)
        if form.is_valid():
            position = 1
            if form.cleaned_data["target"]:
                position = form.cleaned_data["target"].position + 1
            move_down_siblings(position)
            object = Item()
            object.title = form.cleaned_data["title"]
            object.position = position
            object.save()
            return HttpResponse(headers={"HX-Trigger": "refreshList"})
    else:
        template_name = "boxlist/htmx/create.html"
        last = Item.objects.last()
        form = ItemCreateForm(initial={"target": last.id})
        return TemplateResponse(request, template_name, {"form": form})


def add_button(request):
    """Rendered in #add-button when create is dismissed"""

    check_htmx_request(request)
    template_name = "boxlist/htmx/add_button.html"
    return TemplateResponse(request, template_name, {})


def item_sort(request):
    """Updates POSTed position of items, swaps none and
    emits events to refresh items"""

    check_htmx_request(request)
    event_dict = {}
    if "item" in request.POST:
        i = 1
        id_list = request.POST.getlist("item")
        for id in id_list:
            item = get_object_or_404(Item, id=id)
            if not item.position == i:
                item.position = i
                item.save()
                event_dict["refreshItem" + str(item.id)] = "true"
            i += 1
    return HttpResponse(headers={"HX-Trigger": json.dumps(event_dict)})


def item_update(request, pk):
    """Rendered in #item-{{ item.id }}, on success swaps none
    and refreshes #item-{{ item.id }} or #content if position changed.
    If DELETE method, swaps in #item-{{ item.id }}"""

    check_htmx_request(request)
    item = get_object_or_404(Item, id=pk)
    original_position = item.position
    if request.method == "DELETE":
        template_name = "boxlist/htmx/delete.html"
        item.move_following_items()
        item.delete()
        return TemplateResponse(request, template_name, {})
    elif request.method == "POST":
        form = ItemUpdateForm(request.POST)
        if form.is_valid():
            position = original_position
            if form.cleaned_data["target"]:
                position = form.cleaned_data["target"].position
            intercalate_siblings(position, original_position)
            item.title = form.cleaned_data["title"]
            item.position = position
            item.save()
            if not item.position == original_position:
                headers = {"HX-Trigger": "refreshList"}
            else:
                headers = {"HX-Trigger": "refreshItem" + str(item.id)}
            return HttpResponse(headers=headers)
    else:
        template_name = "boxlist/htmx/update.html"
        form = ItemUpdateForm(initial={"title": item.title})
        context = {"object": item, "form": form}
        return TemplateResponse(request, template_name, context)


def item_detail(request, pk):
    """Rendered in #item-{{ item.id }} when update is dismissed or successful"""

    check_htmx_request(request)
    template_name = "boxlist/htmx/detail.html"
    context = {"object": get_object_or_404(Item, id=pk)}
    return TemplateResponse(request, template_name, context)
