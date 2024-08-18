from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("pk", "first_name", "username", "is_staff")
    fieldsets = (
        ("Авторизация", {"fields": ("username", "password")}),
        (
            "Личные данные",
            {"fields": ("last_name", "first_name", "middle_name", "date_joined")},
        ),
    )
