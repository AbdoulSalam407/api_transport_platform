from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Vehicule
from .serializers import VehiculeSerializer


class VehiculeViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des véhicules"""
    
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["type_vehicule", "status"]
    search_fields = ["marque", "modele", "plaque_immatriculation"]
    ordering_fields = ["date_creation", "capacite"]
