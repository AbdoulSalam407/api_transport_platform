from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Passager, Transporteur, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "nom", "prenom", "role", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informations", {"fields": ("username", "nom", "prenom", "role")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "nom", "prenom", "role", "password1", "password2"),
            },
        ),
    )


@admin.register(Passager)
class PassagerAdmin(admin.ModelAdmin):
    list_display = ("user", "telephone")


@admin.register(Transporteur)
class TransporteurAdmin(admin.ModelAdmin):
    list_display = ("user", "nom_compagnie", "statut_validation")
