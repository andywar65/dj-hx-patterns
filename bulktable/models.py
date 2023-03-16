from django.db import models
from django.utils.translation import gettext_lazy as _


class Row(models.Model):
    COLOR = [
        ("light", _("White")),
        ("danger", _("Red")),
        ("success", _("Green")),
        ("primary", _("Blue")),
        ("warning", _("Yellow")),
    ]

    title = models.CharField(
        _("Name"),
        max_length=50,
    )
    color = models.CharField(
        max_length=7,
        choices=COLOR,
    )

    class Meta:
        verbose_name = _("Row")
        verbose_name_plural = _("Rows")

    def __str__(self):
        return self.title
