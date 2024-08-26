from django.contrib import admin
from .models import Specie, SpeciePhoto


class SpeciePhotoInline(admin.StackedInline):
    model = SpeciePhoto
    extra = 1


@admin.register(Specie)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("title", "participants_left")
    search_fields = ("title",)
    inlines = [SpeciePhotoInline]


# @admin.register(SpeciePhoto)
# class SpeciePhotoAdmin(admin.ModelAdmin):
#     list_display = ("specie", "photo")
#     search_fields = ("specie",)
