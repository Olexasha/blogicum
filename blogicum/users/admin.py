from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("about_me",)}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.empty_value_display = "Не задано"
