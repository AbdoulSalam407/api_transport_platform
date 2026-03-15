from django.contrib import admin
from .models import Transport


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ("nom", "type", "plaque_immatriculation", "capacite", "status", "date_creation")
    list_filter = ("status", "type", "date_creation")
    search_fields = ("nom", "plaque_immatriculation")
    readonly_fields = ("date_creation", "date_modification")
    
    fieldsets = (
        ("Informations principales", {
            "fields": ("nom", "type", "plaque_immatriculation", "capacite")
        }),
        ("Statut", {
            "fields": ("status",)
        }),
        ("Dates", {
            "fields": ("date_creation", "date_modification"),
            "classes": ("collapse",)
        }),
    )
