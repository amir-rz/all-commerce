from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from . import models


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["full_name", "phone"]
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal Info"), {"fields": ("full_name",)}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")}
        ),
        (_("Important dates"), {"fields": ("last_login",)})
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "password1", "password2")
        }),
    )

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Token)