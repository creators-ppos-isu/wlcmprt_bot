from django.contrib import admin
from .models import Specie, SpeciePhoto


@admin.register(Specie)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("title", "participants_left")
    search_fields = ("title",)

@admin.register(SpeciePhoto)
class SpeciePhotoAdmin(admin.ModelAdmin):
    list_display = ("specie", "photo")
    search_fields = ("specie",)