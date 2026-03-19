from rest_framework import serializers
from .models import Paiement


class PaiementSerializer(serializers.ModelSerializer):
    """Serializer pour les paiements"""
    
    class Meta:
        model = Paiement
        fields = [
            "id",
            "reservation",
            "montant",
            "methode_paiement",
            "status",
            "reference_transaction",
            "date_paiement",
            "date_confirmation",
        ]
        read_only_fields = ["id", "date_paiement", "date_confirmation"]
