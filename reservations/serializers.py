from rest_framework import serializers
from .models import Reservation, Billet, PointRamassage
from users.serializers import PassagerSerializer
from trajets.serializers import TrajetSerializer


class ReservationSerializer(serializers.ModelSerializer):
    """Sérializer pour Reservation"""
    passager_detail = PassagerSerializer(source='passager', read_only=True)
    trajet_detail = TrajetSerializer(source='trajet', read_only=True)
    statut_affichage = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'passager', 'passager_detail', 'trajet', 'trajet_detail',
            'nombre_places', 'numero_siege', 'prix_total', 'statut',
            'statut_affichage', 'recupere', 'heure_recuperation',
            'date_reservation', 'date_modification'
        ]
        read_only_fields = ['date_reservation', 'date_modification', 'prix_total']
    
    def get_statut_affichage(self, obj):
        """Retourne le statut en français"""
        statuts = {
            'en_attente': 'En attente',
            'confirmee': 'Confirmée',
            'annulee': 'Annulée',
            'terminee': 'Terminée',
        }
        return statuts.get(obj.statut, obj.statut)
    
    def validate(self, data):
        """Validation personnalisée"""
        # Vérifier que le nombre de places est disponible
        trajet = data.get('trajet')
        nombre_places = data.get('nombre_places', 1)
        
        if trajet and not trajet.verifier_places(nombre_places):
            raise serializers.ValidationError(
                f"Plus que {trajet.places_disponibles} places disponibles"
            )
        
        return data


class ReservationCreateSerializer(serializers.ModelSerializer):
    """Sérializer pour la création d'une réservation"""
    
    class Meta:
        model = Reservation
        fields = ['trajet', 'nombre_places', 'numero_siege']
    
    def validate(self, data):
        trajet = data.get('trajet')
        nombre_places = data.get('nombre_places', 1)
        
        if not trajet.verifier_places(nombre_places):
            raise serializers.ValidationError(
                f"Plus que {trajet.places_disponibles} places disponibles"
            )
        
        # Vérifier que le trajet est actif
        if trajet.statut != 'actif':
            raise serializers.ValidationError("Ce trajet n'est pas disponible")
        
        # Vérifier que la date n'est pas passée
        from django.utils import timezone
        if trajet.date_depart < timezone.now():
            raise serializers.ValidationError("Ce trajet est déjà passé")
        
        return data
    
    def create(self, validated_data):
        passager = self.context['request'].user.passager_profile
        trajet = validated_data['trajet']
        nombre_places = validated_data.get('nombre_places', 1)
        
        # Calculer le prix total
        prix_total = trajet.prix_base * nombre_places
        
        reservation = Reservation.objects.create(
            passager=passager,
            prix_total=prix_total,
            **validated_data
        )
        
        return reservation


class BilletSerializer(serializers.ModelSerializer):
    """Sérializer pour Billet"""
    reservation_detail = ReservationSerializer(source='reservation', read_only=True)
    qr_code_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Billet
        fields = ['id', 'reservation', 'reservation_detail', 'code_qr', 'pdf', 'date_emission', 'qr_code_url']
        read_only_fields = ['date_emission']
    
    def get_qr_code_url(self, obj):
        """Retourne l'URL du QR code"""
        request = self.context.get('request')
        if request and obj.code_qr:
            return request.build_absolute_uri(f'/api/billets/qr/{obj.code_qr}/')
        return None


class PointRamassageSerializer(serializers.ModelSerializer):
    """Sérializer pour PointRamassage"""
    reservation_detail = ReservationSerializer(source='reservation', read_only=True)
    coordonnees = serializers.SerializerMethodField()
    
    class Meta:
        model = PointRamassage
        fields = ['id', 'reservation', 'reservation_detail', 'adresse', 
                  'latitude', 'longitude', 'coordonnees', 'instructions', 'date_creation']
        read_only_fields = ['date_creation']
    
    def get_coordonnees(self, obj):
        return {
            'lat': float(obj.latitude) if obj.latitude else None,
            'lng': float(obj.longitude) if obj.longitude else None
        }