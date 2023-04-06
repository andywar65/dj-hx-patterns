from django import forms
from django.forms import ModelChoiceField  # , ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Item


class ItemCreateForm(forms.Form):
    title = forms.CharField(
        label=_("Title"),
        max_length=50,
    )
    after = ModelChoiceField(
        queryset=Item.objects.all(),
        label=_("Add after..."),
        required=False,
    )


class ItemUpdateForm(forms.Form):
    title = forms.CharField(
        label=_("Title"),
        max_length=50,
    )
    replace = ModelChoiceField(
        queryset=Item.objects.all(),
        label=_("Replace with..."),
        required=False,
    )
