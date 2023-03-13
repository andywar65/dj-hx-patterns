from django.db import models
from django.utils.translation import gettext_lazy as _
from tree_queries.models import TreeNode


class Category(TreeNode):
    title = models.CharField(
        _("Name"),
        max_length=50,
    )
    position = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["position"]

    def __str__(self):
        return self.title

    def get_punctuated_index(self):
        qs = self.ancestors(include_self=True).with_tree_fields()
        int_list = qs.values_list("position", flat=True)
        str_list = list(map(str, int_list))
        return ".".join(str_list)

    def get_parent_id(self):
        if not self.parent:
            return None
        return self.parent.id

    def get_next_sibling(self):
        try:
            next = Category.objects.get(
                parent_id=self.get_parent_id(), position=self.position + 1
            )
            return next
        except Category.DoesNotExist:
            return None

    def get_previous_sibling(self):
        if self.position == 0:
            return None
        try:
            prev = Category.objects.get(
                parent_id=self.get_parent_id(), position=self.position - 1
            )
            return prev
        except Category.DoesNotExist:
            return None
