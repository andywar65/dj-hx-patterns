from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from tree_queries.models import TreeNode


class Phase(TreeNode):
    TYPES = [
        ("LP0", _("Other")),
        ("LP1", _("Feasibility study")),
        ("LP2", _("Preliminary design")),
        ("LP3", _("Definitive design")),
        ("LP4", _("Authoring")),
        ("LP5", _("Construction design")),
        ("LP6", _("Tender design")),
        ("LP7", _("Project management")),
        ("LP8", _("Construction supervision")),
        ("LP9", _("Maintenance design")),
    ]

    title = models.CharField(
        _("Name"),
        max_length=50,
    )
    phase_type = models.CharField(
        max_length=4,
        choices=TYPES,
        null=True,
        blank=True,
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
