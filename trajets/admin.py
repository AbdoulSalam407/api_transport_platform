from django.contrib import admin
from .models import Trajet, Etape

@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = ['id', 'depart', 'destination', 'date_depart', 'statut', 'places_disponibles', 'prix_base']  # ← Correction : destination (pas arrivee), statut (pas status)
    list_filter = ['statut', 'date_depart', 'transporteur']  # ← Correction : statut (pas status)
    search_fields = ['depart', 'destination', 'transporteur__utilisateur__email']
    readonly_fields = ['date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('transporteur', 'vehicule', 'chauffeur')
        }),
        ('Itinéraire', {
            'fields': ('depart', 'destination', 'points_arret', 'distance_km')
        }),
        ('Dates et heures', {
            'fields': ('date_depart', 'date_arrivee_estimee', 'date_arrivee_reelle', 'duree_estimee')
        }),
        ('Capacité et prix', {
            'fields': ('places_totales', 'places_disponibles', 'prix_base')
        }),
        ('GPS', {
            'fields': ('latitude_depart', 'longitude_depart', 'latitude_arrivee', 'longitude_arrivee')
        }),
        ('Statut', {
            'fields': ('statut', 'description')
        }),
        ('Dates système', {
            'fields': ('date_creation', 'date_modification')
        }),
    )


@admin.register(Etape)
class EtapeAdmin(admin.ModelAdmin):
    list_display = ['id', 'trajet', 'lieu', 'heure_prevue', 'ordre']
    list_filter = ['trajet', 'ordre']
    search_fields = ['lieu']