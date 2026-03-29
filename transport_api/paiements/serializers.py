from django.db import transaction
from rest_framework import serializers

from reservations.models import ReservationStatut
from reservations.serializers import ReservationSerializer

from .models import Paiement, PaiementStatut


class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = (
            "id",
            "reservation",
            "montant",
            "methode",
            "statut",
            "date_paiement",
        )
        read_only_fields = ("statut", "date_paiement")

    def validate(self, attrs):
        reservation = attrs.get("reservation") or getattr(self.instance, "reservation", None)
        montant = attrs.get("montant")
        if reservation and montant is not None:
            prix = reservation.trajet.prix * reservation.nombre_places
            if montant != prix:
                raise serializers.ValidationError(
                    {"montant": f"Le montant doit correspondre au trajet × places ({prix})."}
                )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        paiement = Paiement.objects.create(**validated_data)
        return paiement
