from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Trajet
from .serializers import TrajetSerializer


class TrajetViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des trajets"""
    
    queryset = Trajet.objects.all()
    serializer_class = TrajetSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "depart", "arrivee"]
    search_fields = ["depart", "arrivee"]
    ordering_fields = ["date_depart", "prix_base"]
    
    @action(detail=False, methods=["get"])
    def disponibles(self, request):
        """Récupérer les trajets disponibles"""
        trajets = Trajet.objects.filter(
            status="planifie",
            places_disponibles__gt=0
        )
        serializer = self.get_serializer(trajets, many=True)
        return Response(serializer.data)
