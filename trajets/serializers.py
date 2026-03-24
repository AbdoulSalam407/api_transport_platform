from rest_framework import serializers
from .models import Trajet, Etape
from users.serializers import TransporteurSerializer


class EtapeSerializer(serializers.ModelSerializer):
    """Sérializer pour Etape"""
    
    class Meta:
        model = Etape
        fields = ['id', 'trajet', 'lieu', 'heure_prevue', 'heure_reelle', 'ordre']


class TrajetSerializer(serializers.ModelSerializer):
    """Sérializer pour Trajet"""
    transporteur_detail = TransporteurSerializer(source='transporteur', read_only=True)
    etapes = EtapeSerializer(many=True, read_only=True)
    places_reservees = serializers.IntegerField(read_only=True)
    taux_remplissage = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Trajet
        fields = [
            'id', 'transporteur', 'transporteur_detail', 'depart', 'destination',
            'date_depart', 'date_arrivee', 'places_totales', 'places_disponibles',
            'places_reservees', 'prix', 'statut', 'description', 'duree_estimee',
            'latitude_depart', 'longitude_depart', 'latitude_arrivee', 'longitude_arrivee',
            'arrets', 'etapes', 'taux_remplissage', 'date_creation', 'date_modification'
        ]
        read_only_fields = ['date_creation', 'date_modification', 'places_reservees', 'taux_remplissage']


class RechercheTrajetSerializer(serializers.Serializer):
    """Sérializer pour la recherche de trajets"""
    depart = serializers.CharField(required=True)
    destination = serializers.CharField(required=True)
    date = serializers.DateField(required=False)
    passagers = serializers.IntegerField(default=1, min_value=1)