import calendar
from datetime import date, timedelta

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from tree_queries.models import TreeNode


class Phase(TreeNode):
    TYPES = [
        ("#dddddd", _("Other")),
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
        default="#dddddd",
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
        prev = Phase.objects.get(
            parent_id=self.get_parent_id(), position=self.position - 1
        )
        return prev

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

    def get_start_end(self):
        start = None
        end = None
        # simple case
        if self.start:
            start = self.start
            end = self.start + timedelta(days=self.duration * 7)
        # complex case
        else:
            # get all ancestors in reverse order
            ancestors = self.ancestors().reverse()
            # delay from parent end
            margin = self.delay
            # walk through ancestors backwards
            for ancestor in ancestors:
                # increment margin
                margin += ancestor.duration
                # stop if ancestor has a start date
                if ancestor.start:
                    # start and end date
                    start = ancestor.start + timedelta(days=margin * 7)
                    end = start + timedelta(days=self.duration * 7)
                    break
                # continue if start date is not found
                margin += ancestor.delay
        return start, end

    def get_popup(self):
        start, end = self.get_start_end()
        popup = _("Type: %(type)s, start: %(start)s, end: %(end)s") % {
            "type": self.get_phase_type_display(),
            "start": start,
            "end": end,
        }
        return popup

    def draw_bar_chart(self, year, month):
        start, end = self.get_start_end()
        chart_start, chart_end = get_chart_start_end(year, month)
        margin, width = get_margin_width(start, end, chart_start, chart_end)
        margin = str(margin) + "%"
        width = str(width) + "%"
        style = (
            "background-color: %(color)s; margin-left: %(margin)s; width: %(width)s"
            % {"color": self.phase_type, "margin": margin, "width": width}
        )
        return style

    def save(self, *args, **kwargs):
        if not self.parent and not self.start:
            self.start = now()
        if self.start:
            self.delay = 0
        super(Phase, self).save(*args, **kwargs)


def get_chart_start_end(year, month):
    if month == 1:
        chart_start = date(year, 1, 1)
        chart_end = date(year, 12, 31)
    else:
        chart_start = date(year, 7, 1)
        chart_end = date(year + 1, 6, 30)
    return chart_start, chart_end


def get_margin_width(start, end, chart_start, chart_end):
    width = 100
    if start <= chart_start:
        margin = 0
    elif start > chart_start and start < chart_end:
        margin = ((start - chart_start).days + 1) / 365 * 100
    else:
        margin = 100
        width = 0
    if width:
        if end < chart_start:
            width = 0
        elif end < chart_end:
            width = 100 - margin - (chart_end - end).days / 365 * 100
        else:
            width = 100 - margin
    return round(margin, 2), round(width, 2)


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


def get_month_dict(year, month):
    month_1 = [1, 2, 3, 4, 5, 6]
    month_2 = [7, 8, 9, 10, 11, 12]
    if month < 7:
        months = month_1 + month_2
    else:
        year += 1
        months = month_2 + month_1
    month_dict = {}
    for m in months:
        actual = False
        if now().year == year and now().month == m:
            actual = True
        month_dict[calendar.month_abbr[m]] = actual
    return month_dict
