from django.contrib import admin
from .models import Paiement


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ("reference_transaction", "montant", "methode_paiement", "status", "date_paiement")
    list_filter = ("status", "methode_paiement", "date_paiement")
    search_fields = ("reference_transaction", "reference_externe")
    readonly_fields = ("date_paiement", "date_confirmation", "date_remboursement")
