from django import forms
from django.forms import ModelChoiceField  # , ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Item

# class ItemCreateForm(ModelForm):
# class Meta:
# model = Item
# exclude = ("position",)


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
