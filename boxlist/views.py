# import json

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from .forms import ItemModelForm
from .models import Item, move_down_siblings


def check_htmx_request(request):
    """Helper function"""

    if not request.htmx:
        raise Http404("Request without HTMX headers")


def item_list_create(request):
    """Lists or creates item, depending on request method:
    GET = List items, renders in #content
    PUT = Open create form, rendered in #add-button
    POST = Create item, redirects to boxlist:list, renders in #content
    DELETE = Dismiss create form, renders in #add-button
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
        form = ItemModelForm(request.POST)
        if form.is_valid():
            position = 1
            move_down_siblings(position)
            object = Item()
            object.title = form.cleaned_data["title"]
            object.position = position
            object.save()
            return HttpResponseRedirect(
                reverse("boxlist:list"), headers={"HX-Request": True}
            )
    elif request.method == "DELETE":
        check_htmx_request(request)
        template_name = "boxlist/htmx/add_button.html"
        return TemplateResponse(request, template_name, {})


def item_sort(request):
    """Updates POSTed position of items, redirects to boxlist:list,
    renders in #content (left previous code in comments)"""

    check_htmx_request(request)
    # event_dict = {}
    if "item" in request.POST:
        i = 1
        id_list = request.POST.getlist("item")
        for id in id_list:
            item = get_object_or_404(Item, id=id)
            if not item.position == i:
                item.position = i
                item.save()
                # event_dict["refreshItem" + str(item.id)] = "true"
            i += 1
    return HttpResponseRedirect(reverse("boxlist:list"), headers={"HX-Request": True})


def item_review_update_delete(request, pk):
    """Manages item, depending on request method,
    renders in #item-{{ item.id }}:
    GET = Reviews item
    PUT = Open update form
    POST = Update item, on success redirects to boxlist:detail
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
        form = ItemModelForm(initial={"title": item.title})
        context = {"object": item, "form": form}
        return TemplateResponse(request, template_name, context)
    elif request.method == "POST":
        form = ItemModelForm(request.POST)
        if form.is_valid():
            item.title = form.cleaned_data["title"]
            item.save()
            return HttpResponseRedirect(
                reverse("boxlist:detail", kwargs={"pk": item.id}),
                headers={"HX-Request": True},
            )
    elif request.method == "DELETE":
        template_name = "boxlist/htmx/delete.html"
        item.move_following_items()
        item.delete()
        return TemplateResponse(request, template_name, {})
