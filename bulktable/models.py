from django.db import models
from django.utils.translation import gettext_lazy as _


class Row(models.Model):
    COLOR = [
        ("#000000", _("White")),
        ("#FF0000", _("Red")),
        ("#00FF00", _("Green")),
        ("#0000FF", _("Blue")),
        ("#00FFFF", _("Yellow")),
    ]

    title = models.CharField(
        _("Name"),
        max_length=50,
    )
    color = models.CharField(
        max_length=7,
        choices=COLOR,
        default="#000000",
    )

    class Meta:
        verbose_name = _("Row")
        verbose_name_plural = _("Rows")

    def __str__(self):
        return self.title
