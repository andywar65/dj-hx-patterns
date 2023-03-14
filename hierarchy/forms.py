from django.forms import ModelForm
from tree_queries.forms import TreeNodeChoiceField

from .models import Category


class CategoryCreateForm(ModelForm):
    parent = TreeNodeChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Category
        exclude = [
            "position",
        ]
