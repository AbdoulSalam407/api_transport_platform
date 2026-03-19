from django.contrib import admin
from .models import Trajet


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = ("depart", "arrivee", "date_depart", "status", "places_disponibles")
    list_filter = ("status", "date_depart")
    search_fields = ("depart", "arrivee")
    readonly_fields = ("date_creation", "date_modification")
