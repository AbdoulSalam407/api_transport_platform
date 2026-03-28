from rest_framework import serializers
from .models import Trajet


class TrajetSerializer(serializers.ModelSerializer):
    """Serializer pour les trajets"""
    
    vehicule_detail = serializers.StringRelatedField(source="vehicule", read_only=True)
    transporteur_detail = serializers.CharField(source="transporteur.get_full_name", read_only=True)
    
    class Meta:
        model = Trajet
        fields = [
            "id",
            "vehicule",
            "vehicule_detail",
            "transporteur",
            "transporteur_detail",
            "ville_depart",
            "ville_arrivee",
            "distance_km",
            "duree_estimee",
            "date_depart",
            "heure_depart",
            "prix",
            "nombre_places_disponibles",
            "places_totales",
            "statut",
            "points_arret",
            "date_creation",
            "date_modification",
        ]
        read_only_fields = ["id", "date_creation", "date_modification"]
