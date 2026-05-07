from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Sérializer pour Notification"""
    type_affichage = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'utilisateur', 'reservation', 'type', 'type_affichage',
            'titre', 'message', 'est_lu', 'data', 'date_creation', 'date_lecture'
        ]
        read_only_fields = ['date_creation', 'date_lecture']
    
    def get_type_affichage(self, obj):
        types = {
            'reservation': 'Réservation',
            'rappel': 'Rappel',
            'depart_imminent': 'Départ imminent',
            'annulation': 'Annulation',
            'modification': 'Modification',
            'promotion': 'Promotion',
            'systeme': 'Système',
        }
        return types.get(obj.type, obj.type)


class NotificationMarquerLueSerializer(serializers.Serializer):
    """Sérializer pour marquer une notification comme lue"""
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    tout_marquer = serializers.BooleanField(default=False)