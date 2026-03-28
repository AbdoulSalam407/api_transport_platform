from rest_framework import serializers
from .models import Paiement, TransactionLog
from reservations.serializers import ReservationSerializer


class PaiementSerializer(serializers.ModelSerializer):
    """Sérializer pour Paiement"""
    reservation_detail = ReservationSerializer(source='reservation', read_only=True)
    statut_affichage = serializers.SerializerMethodField()
    methode_affichage = serializers.SerializerMethodField()
    
    class Meta:
        model = Paiement
        fields = [
            'id', 'utilisateur', 'reservation', 'reservation_detail',
            'montant', 'methode', 'methode_affichage', 'statut',
            'statut_affichage', 'transaction_id', 'reference_externe',
            'date_creation', 'date_maj', 'date_validation'
        ]
        read_only_fields = ['date_creation', 'date_maj', 'date_validation', 'transaction_id']
    
    def get_statut_affichage(self, obj):
        statuts = {
            'en_attente': 'En attente',
            'en_cours': 'En cours',
            'reussi': 'Réussi',
            'echoue': 'Échoué',
            'rembourse': 'Remboursé',
        }
        return statuts.get(obj.statut, obj.statut)
    
    def get_methode_affichage(self, obj):
        methodes = {
            'carte': 'Carte bancaire',
            'mobile_money': 'Mobile Money',
            'paypal': 'PayPal',
            'especes': 'Espèces',
        }
        return methodes.get(obj.methode, obj.methode)


class PaiementCreateSerializer(serializers.ModelSerializer):
    """Sérializer pour la création d'un paiement"""
    
    class Meta:
        model = Paiement
        fields = ['reservation', 'methode', 'montant']
    
    def validate(self, data):
        reservation = data.get('reservation')
        montant = data.get('montant')
        
        if montant != reservation.prix_total:
            raise serializers.ValidationError(
                f"Le montant doit être de {reservation.prix_total}€"
            )
        
        if reservation.statut != 'en_attente':
            raise serializers.ValidationError(
                "Cette réservation ne peut pas être payée"
            )
        
        return data


class TransactionLogSerializer(serializers.ModelSerializer):
    """Sérializer pour TransactionLog"""
    
    class Meta:
        model = TransactionLog
        fields = ['id', 'paiement', 'action', 'statut', 'message', 'data', 'date_creation']