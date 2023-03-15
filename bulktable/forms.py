from django.forms import ModelForm

from .models import Row


class RowCreateForm(ModelForm):
    class Meta:
        model = Row
        fields = ("title", "color")
