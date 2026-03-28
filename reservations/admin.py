from django.contrib import admin
from .models import Reservation, Billet, PointRamassage

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'passager', 'trajet', 'nombre_places', 'prix_total', 'statut', 'date_reservation']  # ← Correction : passager (pas client), statut (pas status)
    list_filter = ['statut', 'recupere', 'date_reservation']  # ← Correction : statut (pas status)
    search_fields = ['passager__utilisateur__email', 'passager__utilisateur__nom', 'trajet__depart']
    readonly_fields = ['date_reservation', 'date_modification']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('passager', 'trajet', 'nombre_places', 'numero_siege')
        }),
        ('Prix et statut', {
            'fields': ('prix_total', 'statut')
        }),
        ('Récupération', {
            'fields': ('recupere', 'heure_recuperation')
        }),
        ('Dates', {
            'fields': ('date_reservation', 'date_modification')
        }),
    )


@admin.register(Billet)
class BilletAdmin(admin.ModelAdmin):
    list_display = ['id', 'reservation', 'code_qr', 'date_emission']
    search_fields = ['code_qr', 'reservation__passager__utilisateur__email']
    readonly_fields = ['date_emission']


@admin.register(PointRamassage)
class PointRamassageAdmin(admin.ModelAdmin):
    list_display = ['id', 'reservation', 'adresse', 'date_creation']
    list_filter = ['date_creation']
    search_fields = ['adresse', 'reservation__passager__utilisateur__email']