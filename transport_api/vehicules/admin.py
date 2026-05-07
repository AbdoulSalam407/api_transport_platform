from django.contrib import admin

from .models import Vehicule


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ("immatriculation", "type", "capacite", "transporteur")
