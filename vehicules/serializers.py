from rest_framework import serializers
from .models import Vehicule


class VehiculeSerializer(serializers.ModelSerializer):
    """Serializer pour les véhicules"""
    
    class Meta:
        model = Vehicule
        fields = [
            "id",
            "chauffeur",
            "marque",
            "modele",
            "plaque_immatriculation",
            "type_vehicule",
            "capacite",
            "status",
            "couleur",
            "photo",
            "kilometrage",
        ]
        read_only_fields = ["id"]
