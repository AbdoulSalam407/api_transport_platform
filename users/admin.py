from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "role", "is_verified", "date_joined")
    list_filter = ("role", "is_verified", "date_joined")
    search_fields = ("username", "email", "phone_number")
    readonly_fields = ("date_joined", "last_login")
    
    fieldsets = (
        ("Informations personnelles", {
            "fields": ("username", "first_name", "last_name", "email", "phone_number")
        }),
        ("Profil", {
            "fields": ("role", "profile_picture", "bio", "is_verified")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Dates", {
            "fields": ("date_joined", "last_login"),
            "classes": ("collapse",)
        }),
    )
