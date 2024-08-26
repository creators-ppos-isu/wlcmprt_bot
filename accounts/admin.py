from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Specie


class SpecieFilter(admin.SimpleListFilter):
    title = "Антилокации"
    parameter_name = "specie"

    def lookups(self, request, model_admin):
        return Specie.objects.all().values_list("pk", "title")

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(spacie_id=self.value())
        return queryset


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "pk",
        "first_name",
        "last_name",
        "middle_name",
        "specie",
        "username",
        "is_staff",
    )
    fieldsets = (
        ("Авторизация", {"fields": ("username", "password")}),
        (
            "Личные данные",
            {"fields": ("last_name", "first_name", "middle_name", "date_joined")},
        ),
        (None, {"fields": ("spacie",)}),
    )

    list_filter = ("is_superuser", SpecieFilter)

    def specie(self, obj):
        return obj.spacie
