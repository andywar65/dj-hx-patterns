from django.db import models
from django.utils.translation import gettext_lazy as _


class Item(models.Model):
    title = models.CharField(
        _("Name"),
        max_length=50,
    )
    position = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        ordering = [
            "position",
        ]

    def __str__(self):
        return self.title

    def get_next_item(self):
        try:
            next = Item.objects.get(position=self.position + 1)
            return next
        except Item.DoesNotExist:
            return None

    def get_previous_item(self):
        try:
            prev = Item.objects.get(position=self.position - 1)
            return prev
        except Item.DoesNotExist:
            return None

    def move_following_items(self):
        """Used when an item is deleted.
        Items with greater position than (self) are
        moved up the ladder.
        """
        following = Item.objects.filter(position__gt=self.position)
        for item in following:
            item.position -= 1
            item.save()
