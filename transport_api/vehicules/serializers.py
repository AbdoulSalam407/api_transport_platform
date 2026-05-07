from rest_framework import serializers

from .models import Vehicule


class VehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = (
            "id",
            "immatriculation",
            "capacite",
            "type",
            "latitude",
            "longitude",
            "transporteur",
        )
