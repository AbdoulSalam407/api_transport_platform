from django.contrib import admin
from .models import Paiement, TransactionLog

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['id', 'utilisateur', 'reservation', 'montant', 'methode', 'statut', 'date_creation']
    list_filter = ['methode', 'statut', 'date_creation']  # ← Correction : methode (pas methode_paiement)
    search_fields = ['transaction_id', 'utilisateur__email', 'utilisateur__nom']
    readonly_fields = ['date_creation', 'date_maj', 'date_validation']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('utilisateur', 'reservation', 'montant', 'methode')
        }),
        ('Statut', {
            'fields': ('statut', 'transaction_id', 'reference_externe')
        }),
        ('Données', {
            'fields': ('data_paiement',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_maj', 'date_validation')
        }),
    )


@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'paiement', 'action', 'statut', 'date_creation']
    list_filter = ['action', 'statut', 'date_creation']
    search_fields = ['paiement__transaction_id', 'message']
    readonly_fields = ['date_creation']