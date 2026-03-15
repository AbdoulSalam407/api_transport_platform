from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Paiement
from .serializers import PaiementSerializer


class PaiementViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour la consultation des paiements (lecture seule)"""
    
    serializer_class = PaiementSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "methode_paiement"]
    ordering_fields = ["date_paiement", "montant"]
    
    def get_queryset(self):
        """Retourner les paiements de l'utilisateur connecté"""
        user = self.request.user
        if user.is_staff or user.role == "admin":
            return Paiement.objects.all()
        return Paiement.objects.filter(client=user)
