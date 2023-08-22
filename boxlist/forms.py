from django.forms import ModelForm

from .models import Item


class ItemModelForm(ModelForm):
    class Meta:
        model = Item
        fields = ("title",)
