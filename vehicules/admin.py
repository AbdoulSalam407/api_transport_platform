from django.contrib import admin
from .models import Vehicule


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ("marque", "modele", "plaque_immatriculation", "type_vehicule", "capacite", "status")
    list_filter = ("type_vehicule", "status", "date_creation")
    search_fields = ("marque", "modele", "plaque_immatriculation")
    readonly_fields = ("date_creation", "date_modification", "kilometrage")
