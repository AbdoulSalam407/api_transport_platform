from rest_framework import serializers
from .models import Trajet, Etape
from users.serializers import TransporteurSerializer
from core.validation import VALIDATION_STATUT_LABELS

VALIDATION_FIELDS = [
    'validation_statut', 'validation_statut_affichage', 'motif_rejet', 'date_validation',
]


class EtapeSerializer(serializers.ModelSerializer):
    """Sérializer pour Etape"""
    
    class Meta:
        model = Etape
        fields = ['id', 'trajet', 'lieu', 'heure_prevue', 'heure_reelle', 'ordre']


class TrajetBriefSerializer(serializers.ModelSerializer):
    """Trajet allégé pour listes et réservations."""
    validation_statut_affichage = serializers.SerializerMethodField()
    places_reservees = serializers.SerializerMethodField()

    class Meta:
        model = Trajet
        fields = [
            'id', 'depart', 'destination', 'date_depart', 'date_arrivee_estimee',
            'places_totales', 'places_disponibles', 'places_reservees', 'prix_base', 'statut',
            'validation_statut', 'validation_statut_affichage', 'motif_rejet',
        ]
        read_only_fields = ['validation_statut', 'motif_rejet', 'places_reservees']

    def get_validation_statut_affichage(self, obj):
        return VALIDATION_STATUT_LABELS.get(obj.validation_statut, obj.validation_statut)

    def get_places_reservees(self, obj):
        return obj.places_reservees


class TrajetSerializer(serializers.ModelSerializer):
    """Sérializer pour Trajet"""
    transporteur_detail = TransporteurSerializer(source='transporteur', read_only=True)
    etapes = EtapeSerializer(many=True, read_only=True)
    places_reservees = serializers.IntegerField(read_only=True)
    taux_remplissage = serializers.FloatField(read_only=True)
    validation_statut_affichage = serializers.SerializerMethodField()
    
    class Meta:
        model = Trajet
        fields = [
            'id', 'transporteur', 'transporteur_detail', 'vehicule', 'chauffeur',
            'depart', 'destination', 'date_depart', 'date_arrivee_estimee',
            'date_arrivee_reelle', 'places_totales', 'places_disponibles',
            'places_reservees', 'prix_base', 'distance_km', 'statut', 'description',
            'duree_estimee', 'latitude_depart', 'longitude_depart', 'latitude_arrivee',
            'longitude_arrivee', 'points_arret', 'arrets', 'etapes', 'taux_remplissage',
            'date_creation', 'date_modification',
            'validation_statut', 'validation_statut_affichage', 'motif_rejet', 'date_validation',
        ]
        read_only_fields = [
            'date_creation', 'date_modification', 'places_reservees', 'taux_remplissage',
            'transporteur', 'validation_statut', 'motif_rejet', 'date_validation', 'valide_par',
        ]

    def get_validation_statut_affichage(self, obj):
        return VALIDATION_STATUT_LABELS.get(obj.validation_statut, obj.validation_statut)

    def validate(self, attrs):
        places_totales = attrs.get(
            'places_totales',
            getattr(self.instance, 'places_totales', None),
        )
        places_disponibles = attrs.get('places_disponibles')

        if places_totales is not None:
            if places_disponibles is None:
                attrs['places_disponibles'] = places_totales
            elif places_disponibles > places_totales:
                raise serializers.ValidationError({
                    'places_disponibles': 'Ne peut pas dépasser le nombre total de places.',
                })
            elif self.instance is None and places_disponibles == 0 and places_totales > 0:
                attrs['places_disponibles'] = places_totales

        if self.instance is not None and places_totales is not None:
            reservees = self.instance.places_reservees
            if places_totales < reservees:
                raise serializers.ValidationError({
                    'places_totales': (
                        f'Impossible : {reservees} place(s) déjà réservée(s). '
                        f'Minimum : {reservees}.'
                    ),
                })
            if 'places_disponibles' not in attrs:
                attrs['places_disponibles'] = places_totales - reservees

        return attrs

    def create(self, validated_data):
        validated_data['places_disponibles'] = validated_data.get(
            'places_disponibles',
            validated_data['places_totales'],
        )
        if validated_data['places_disponibles'] == 0 and validated_data['places_totales'] > 0:
            validated_data['places_disponibles'] = validated_data['places_totales']
        return super().create(validated_data)


class RechercheTrajetSerializer(serializers.Serializer):
    """Sérializer pour la recherche de trajets"""
    depart = serializers.CharField(required=True)
    destination = serializers.CharField(required=True)
    date = serializers.DateField(required=False)
    passagers = serializers.IntegerField(default=1, min_value=1)