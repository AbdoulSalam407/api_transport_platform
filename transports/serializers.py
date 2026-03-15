from rest_framework import serializers
from .models import Transport


class TransportSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Transport"""
    
    class Meta:
        model = Transport
        fields = [
            "id",
            "nom",
            "type",
            "plaque_immatriculation",
            "capacite",
            "status",
            "date_creation",
            "date_modification",
        ]
        read_only_fields = ["id", "date_creation", "date_modification"]
