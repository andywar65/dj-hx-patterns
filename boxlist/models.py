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
        return "%(pos)d - %(title)s" % {"pos": self.id, "title": self.title}

    def move_following_items(self):
        """Used when an item is deleted.
        Items with greater position than (self) are
        moved up the ladder.
        """
        following = Item.objects.filter(position__gt=self.position)
        for item in following:
            item.position -= 1
            item.save()


def move_down_siblings(position):
    """Used when an item is added.
    Items with greater / equal position are
    moved down the ladder.
    """
    siblings = Item.objects.filter(position__gte=position)
    for sibling in siblings:
        sibling.position += 1
        sibling.save()


def intercalate_siblings(new, original):
    if new == original:
        return new
    if original > new:
        siblings = Item.objects.filter(position__gte=new).exclude(
            position__gte=original
        )
        for sibling in siblings:
            sibling.position += 1
            sibling.save()
    else:
        siblings = Item.objects.filter(position__lte=new).exclude(
            position__lte=original
        )
        for sibling in siblings:
            sibling.position -= 1
            sibling.save()
