from django.contrib import admin

from .models import Row


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_display = ("title", "color")
