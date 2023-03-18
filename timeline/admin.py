from django.contrib import admin

from .models import Phase


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ("title", "parent", "position")
    list_filter = ("parent",)
    list_editable = ("position",)
