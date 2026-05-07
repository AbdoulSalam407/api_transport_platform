from django.contrib import admin

from .models import Paiement


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ("id", "reservation", "montant", "statut", "date_paiement")
