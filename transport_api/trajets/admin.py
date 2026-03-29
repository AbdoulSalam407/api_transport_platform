from django.contrib import admin

from .models import Trajet


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = ("ville_depart", "ville_arrivee", "date_depart", "prix", "statut")
