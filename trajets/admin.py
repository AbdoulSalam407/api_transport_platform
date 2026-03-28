from django.contrib import admin
from .models import Trajet


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = ("ville_depart", "ville_arrivee", "date_depart", "heure_depart", "statut", "nombre_places_disponibles", "prix")
    list_filter = ("statut", "date_depart", "ville_depart", "ville_arrivee")
    search_fields = ("ville_depart", "ville_arrivee")
    readonly_fields = ("date_creation", "date_modification")
    fieldsets = (
        ("Informations de localisation", {
            "fields": ("ville_depart", "ville_arrivee", "distance_km", "duree_estimee", "points_arret")
        }),
        ("Dates et heures", {
            "fields": ("date_depart", "heure_depart", "date_arrivee_estimee", "date_arrivee_reelle")
        }),
        ("Tarification et places", {
            "fields": ("prix", "nombre_places_disponibles", "places_totales")
        }),
        ("Relations", {
            "fields": ("vehicule", "transporteur")
        }),
        ("Statut et informations", {
            "fields": ("statut", "date_creation", "date_modification")
        }),
    )
