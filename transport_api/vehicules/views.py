from rest_framework import permissions, viewsets

from users.models import Role

from .models import Vehicule
from .serializers import VehiculeSerializer


class VehiculeViewSet(viewsets.ModelViewSet):
    queryset = Vehicule.objects.select_related("transporteur").all()
    serializer_class = VehiculeSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != Role.TRANSPORTEUR:
            raise permissions.PermissionDenied("Seuls les transporteurs peuvent créer un véhicule.")
        serializer.save(transporteur=user.transporteur_profile)

    def perform_update(self, serializer):
        vehicule = self.get_object()
        if self.request.user.role != Role.TRANSPORTEUR:
            raise permissions.PermissionDenied()
        if vehicule.transporteur_id != self.request.user.transporteur_profile.pk:
            raise permissions.PermissionDenied("Ce véhicule ne vous appartient pas.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != Role.TRANSPORTEUR:
            raise permissions.PermissionDenied()
        if instance.transporteur_id != self.request.user.transporteur_profile.pk:
            raise permissions.PermissionDenied()
        instance.delete()
