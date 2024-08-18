from django.contrib import admin
from .models import Specie


@admin.register(Specie)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("title", "participants_left")
    search_fields = ("title",)