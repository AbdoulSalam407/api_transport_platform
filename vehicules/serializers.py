from rest_framework import serializers
from .models import Marque, Modele, Vehicule
from users.serializers import TransporteurSerializer


class MarqueSerializer(serializers.ModelSerializer):
    """Sérializer pour Marque"""
    nombre_modeles = serializers.SerializerMethodField()
    
    class Meta:
        model = Marque
        fields = ['id', 'nom', 'logo', 'nombre_modeles']
    
    def get_nombre_modeles(self, obj):
        return obj.modeles.count()


class ModeleSerializer(serializers.ModelSerializer):
    """Sérializer pour Modele"""
    marque_nom = serializers.CharField(source='marque.nom', read_only=True)
    
    class Meta:
        model = Modele
        fields = ['id', 'marque', 'marque_nom', 'nom', 'nombre_places']


class VehiculeSerializer(serializers.ModelSerializer):
    """Sérializer pour Vehicule"""
    transporteur_detail = TransporteurSerializer(source='transporteur', read_only=True)
    modele_detail = ModeleSerializer(source='modele', read_only=True)
    est_disponible = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Vehicule
        fields = [
            'id', 'transporteur', 'transporteur_detail', 'modele', 'modele_detail',
            'immatriculation', 'couleur', 'annee', 'disponible',
            'en_maintenance', 'est_disponible', 'climatisation', 'wifi',
            'prise_usb', 'espace_bagages', 'photo_principale', 'date_ajout'
        ]
        read_only_fields = ['date_ajout', 'transporteur']