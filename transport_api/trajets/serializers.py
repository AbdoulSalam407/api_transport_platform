from rest_framework import serializers

from .models import Trajet


class TrajetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trajet
        fields = (
            "id",
            "ville_depart",
            "ville_arrivee",
            "date_depart",
            "heure_depart",
            "prix",
            "nombre_places_disponibles",
            "statut",
            "vehicule",
            "transporteur",
        )
