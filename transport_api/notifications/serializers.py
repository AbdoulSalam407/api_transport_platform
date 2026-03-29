from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "user", "message", "type", "date_envoi")
        read_only_fields = ("user", "date_envoi")
