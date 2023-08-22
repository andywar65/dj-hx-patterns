import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .forms import ItemCreateForm, ItemModelForm, ItemUpdateForm  # noqa
from .models import Item, intercalate_siblings, move_down_siblings


def check_htmx_request(request):
    """Helper function"""

    if not request.htmx:
        raise Http404("Request without HTMX headers")


def item_list_create(request):
    """Lists or creates item, depending on request method:
    GET = List items, rendered in #content
    PUT = Open create form, rendered in #add-button
    POST = Create item, swaps none and triggers list refresh
    DELETE = Dismiss create form, rendered in #add-button
    """

    if request.method == "GET":
        template_name = "boxlist/htmx/list.html"
        if not request.htmx:
            template_name = template_name.replace("htmx/", "")
        context = {"object_list": Item.objects.all()}
        return TemplateResponse(request, template_name, context)
    elif request.method == "PUT":
        check_htmx_request(request)
        template_name = "boxlist/htmx/create.html"
        form = ItemModelForm()
        return TemplateResponse(request, template_name, {"form": form})
    elif request.method == "POST":
        check_htmx_request(request)
        form = ItemCreateForm(request.POST)
        if form.is_valid():
            position = 1
            move_down_siblings(position)
            object = Item()
            object.title = form.cleaned_data["title"]
            object.position = position
            object.save()
            return HttpResponse(headers={"HX-Trigger": "refreshList"})
    elif request.method == "DELETE":
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


def item_review_update_delete(request, pk):
    """Manages item, depending on request method,
    rendered in #item-{{ item.id }}:
    GET = Reviews item
    PUT = Open update form
    POST = Update item, on success swaps none
    and refreshes #item-{{ item.id }} or #content if position changed
    DELETE = Deletes item
    """

    check_htmx_request(request)
    item = get_object_or_404(Item, id=pk)
    if request.method == "GET":
        template_name = "boxlist/htmx/detail.html"
        context = {"object": item}
        return TemplateResponse(request, template_name, context)
    elif request.method == "PUT":
        template_name = "boxlist/htmx/update.html"
        form = ItemUpdateForm(initial={"title": item.title})
        context = {"object": item, "form": form}
        return TemplateResponse(request, template_name, context)
    elif request.method == "POST":
        original_position = item.position
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
    elif request.method == "DELETE":
        template_name = "boxlist/htmx/delete.html"
        item.move_following_items()
        item.delete()
        return TemplateResponse(request, template_name, {})
