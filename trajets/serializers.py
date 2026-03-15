from rest_framework import serializers
from .models import Trajet


class TrajetSerializer(serializers.ModelSerializer):
    """Serializer pour les trajets"""
    
    vehicule_detail = serializers.StringRelatedField(source="vehicule", read_only=True)
    chauffeur_detail = serializers.CharField(source="chauffeur.get_full_name", read_only=True)
    
    class Meta:
        model = Trajet
        fields = [
            "id",
            "vehicule",
            "vehicule_detail",
            "chauffeur",
            "chauffeur_detail",
            "depart",
            "arrivee",
            "distance_km",
            "duree_estimee",
            "date_depart",
            "price_base",
            "places_disponibles",
            "places_totales",
            "status",
            "points_arret",
        ]
        read_only_fields = ["id"]
