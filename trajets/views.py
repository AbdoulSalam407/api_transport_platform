from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Trajet, Etape
from .serializers import TrajetSerializer, EtapeSerializer, RechercheTrajetSerializer
from core.permissions import IsAdmin, IsTransporteur, IsAdminOrTransporteur


class TrajetViewSet(viewsets.ModelViewSet):
    """CRUD pour les trajets"""
    queryset = Trajet.objects.all()
    serializer_class = TrajetSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrTransporteur()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
        queryset = Trajet.objects.filter(statut='actif', date_depart__gte=timezone.now())
        
        # Filtrer par paramètres
        depart = self.request.query_params.get('depart', None)
        destination = self.request.query_params.get('destination', None)
        date = self.request.query_params.get('date', None)
        
        if depart:
            queryset = queryset.filter(depart__icontains=depart)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if date:
            queryset = queryset.filter(date_depart__date=date)
        
        return queryset
    
    def perform_create(self, serializer):
        transporteur = self.request.user.transporteur_profile
        serializer.save(transporteur=transporteur)


class EtapeViewSet(viewsets.ModelViewSet):
    """CRUD pour les étapes"""
    queryset = Etape.objects.all()
    serializer_class = EtapeSerializer
    permission_classes = [IsAdminOrTransporteur]


class RechercherTrajetView(generics.ListAPIView):
    """Rechercher des trajets"""
    serializer_class = TrajetSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Trajet.objects.filter(
            statut='actif',
            date_depart__gte=timezone.now(),
            places_disponibles__gt=0
        )
        
        depart = self.request.query_params.get('depart')
        destination = self.request.query_params.get('destination')
        date = self.request.query_params.get('date')
        
        if depart:
            queryset = queryset.filter(depart__icontains=depart)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if date:
            queryset = queryset.filter(date_depart__date=date)
        
        return queryset


class VerifierPlacesView(APIView):
    """Vérifier les places disponibles"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, pk):
        try:
            trajet = Trajet.objects.get(id=pk)
            return Response({
                'places_disponibles': trajet.places_disponibles,
                'places_totales': trajet.places_totales,
                'taux_remplissage': trajet.taux_remplissage
            })
        except Trajet.DoesNotExist:
            return Response(
                {'error': 'Trajet non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )


class TrajetsParTransporteurView(generics.ListAPIView):
    """Lister les trajets d'un transporteur"""
    serializer_class = TrajetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        transporteur_id = self.kwargs['transporteur_id']
        return Trajet.objects.filter(transporteur_id=transporteur_id)