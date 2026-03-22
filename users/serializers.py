from rest_framework import serializers
from .models import CustomUser, Passager, Transporteur

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'telephone']

class PassagerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    
    class Meta:
        model = Passager
        fields = '__all__'

class TransporteurSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    
    class Meta:
        model = Transporteur
        fields = '__all__'