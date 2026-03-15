from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer pour les notifications"""
    
    class Meta:
        model = Notification
        fields = [
            "id",
            "titre",
            "message",
            "type_notification",
            "is_read",
            "lien",
            "date_creation",
        ]
        read_only_fields = ["id", "date_creation"]
