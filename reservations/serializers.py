from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer pour les réservations"""
    
    trajet_detail = serializers.StringRelatedField(source="trajet", read_only=True)
    client_detail = serializers.CharField(source="client.get_full_name", read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            "id",
            "client",
            "client_detail",
            "trajet",
            "trajet_detail",
            "nombre_places",
            "prix_total",
            "status",
            "notes",
            "date_reservation",
        ]
        read_only_fields = ["id", "date_reservation", "prix_total"]
