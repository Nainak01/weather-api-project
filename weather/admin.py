from .models import *
from django.contrib import admin


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    """Admin configuration for Station model."""

    search_fields = ("id", "name")
    list_display = ("id", "name")


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """Admin configuration for Record model."""

    search_fields = ("station__name",)
    list_display = (
        "id",
        "date",
        "max_temp",
        "min_temp",
        "precipitation",
        "station",
    )


@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
    """Admin configuration for Stats model."""

    search_fields = ("station__name",)
    list_display = (
        "id",
        "avg_max_temp",
        "avg_min_temp",
        "total_precipitation",
        "year",
        "station",
    )
