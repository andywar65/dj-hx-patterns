from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from tree_queries.models import TreeNode


class Phase(TreeNode):
    TYPES = [
        ("#ffffff", _("Other")),
        ("#e3342f", _("Feasibility study")),
        ("#f6993f", _("Preliminary design")),
        ("#ffed4a", _("Definitive design")),
        ("#38c172", _("Authoring")),
        ("#4dc0b5", _("Construction design")),
        ("#3490dc", _("Tender design")),
        ("#6574cd", _("Project management")),
        ("#9561e2", _("Construction supervision")),
        ("#f66d9b", _("Maintenance design")),
    ]

    title = models.CharField(
        _("Name"),
        max_length=50,
    )
    phase_type = models.CharField(
        max_length=7,
        choices=TYPES,
        default="#ffffff",
    )
    position = models.PositiveIntegerField(default=0)
    start = models.DateField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=1, help_text=_("In weeks"))
    delay = models.IntegerField(default=0, help_text=_("In weeks"))

    class Meta:
        verbose_name = _("Phase")
        verbose_name_plural = _("Phases")
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
            next = Phase.objects.get(
                parent_id=self.get_parent_id(), position=self.position + 1
            )
            return next
        except Phase.DoesNotExist:
            return None

    def get_previous_sibling(self):
        if self.position == 0:
            return None
        try:
            prev = Phase.objects.get(
                parent_id=self.get_parent_id(), position=self.position - 1
            )
            return prev
        except Phase.DoesNotExist:
            return None

    def move_down(self):
        next = self.get_next_sibling()
        if next:
            self.position += 1
            self.save()
            next.position -= 1
            next.save()

    def move_up(self):
        prev = self.get_previous_sibling()
        if prev:
            self.position -= 1
            self.save()
            prev.position += 1
            prev.save()

    def draw_bar_chart(self):
        width = str(self.duration / 52 * 100) + "%"
        if self.start:
            margin = str(self.start.isocalendar().week / 52 * 100) + "%"
        else:
            ancestors = self.ancestors().reverse()
            margin = self.delay
            for ancestor in ancestors:
                margin += ancestor.duration
                if ancestor.start:
                    margin += ancestor.start.isocalendar().week
                    margin = str(margin / 52 * 100) + "%"
                    break
                margin += ancestor.delay
        return (
            "background-color: %(color)s; margin-left: %(margin)s; width: %(width)s"
            % {"color": self.phase_type, "margin": margin, "width": width}
        )

    def save(self, *args, **kwargs):
        if not self.parent and not self.start:
            self.start = now()
        # import datetime
        # datetime.date(2010, 6, 16).isocalendar().week
        if self.start:
            self.delay = 0
        super(Phase, self).save(*args, **kwargs)


def get_position_by_parent(parent):
    if not parent:
        return Phase.objects.filter(parent_id=None).count()
    return parent.children.count()


def move_younger_siblings(parent, position):
    if not parent:
        siblings = Phase.objects.filter(parent_id=None, position__gt=position)
    else:
        siblings = parent.children.filter(position__gt=position)
    for sibling in siblings:
        sibling.position -= 1
        sibling.save()
