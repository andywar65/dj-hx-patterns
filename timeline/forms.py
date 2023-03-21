from django.forms import ModelForm
from tree_queries.forms import TreeNodeChoiceField

from .models import Phase


class PhaseCreateForm(ModelForm):
    parent = TreeNodeChoiceField(queryset=Phase.objects.all(), required=False)

    class Meta:
        model = Phase
        exclude = ("position",)
