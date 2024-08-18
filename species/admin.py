from django.contrib import admin
from .models import Specie

# Register your models here.

@admin.register(Specie)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("title", "participants_count")
    search_fields = ("title",)