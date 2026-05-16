from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Count, Q, F
from .models import Trajet, Etape
from .serializers import TrajetSerializer, EtapeSerializer, RechercheTrajetSerializer
from core.permissions import IsAdmin, IsTransporteur, IsAdminOrTransporteur


# ==================== PAGINATION ====================
class StandardPagination(PageNumberPagination):
    """Pagination standardisée pour tous les endpoints"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


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
    """Lister les trajets d'un transporteur (Par ID) - AVEC PAGINATION"""
    serializer_class = TrajetSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination
    
    def get_queryset(self):
        transporteur_id = self.kwargs['transporteur_id']
        queryset = Trajet.objects.filter(transporteur_id=transporteur_id).order_by('-date_depart')
        
        # Filtrer par statut si fourni
        statut = self.request.query_params.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        # Filtrer par date (trajets futurs par défaut)
        future_only = self.request.query_params.get('future_only', 'true').lower() == 'true'
        if future_only:
            queryset = queryset.filter(date_depart__gte=timezone.now())
        
        return queryset


class MesTrajetsView(generics.ListAPIView):
    """Lister MES trajets (transporteur connecté) - AVEC PAGINATION"""
    serializer_class = TrajetSerializer
    permission_classes = [IsTransporteur]
    pagination_class = StandardPagination
    
    def get_queryset(self):
        transporteur = self.request.user.transporteur_profile
        queryset = Trajet.objects.filter(transporteur=transporteur).order_by('-date_depart')
        
        # Filtrer par statut si fourni
        statut = self.request.query_params.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        # Filtrer par date (trajets futurs par défaut)
        future_only = self.request.query_params.get('future_only', 'true').lower() == 'true'
        if future_only:
            queryset = queryset.filter(date_depart__gte=timezone.now())
        
        return queryset


class StatistiquesGlobalesView(APIView):
    """Statistiques globales pour la home page"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            # Statistiques de base
            total_trajets = Trajet.objects.filter(
                statut='actif',
                date_depart__gte=timezone.now()
            ).count()
            
            total_trajets_tous = Trajet.objects.all().count()
            trajets_aujourd_hui = Trajet.objects.filter(
                date_depart__date=timezone.now().date()
            ).count()
            
            # Trajets avec places disponibles
            trajets_disponibles = Trajet.objects.filter(
                statut='actif',
                places_disponibles__gt=0,
                date_depart__gte=timezone.now()
            ).count()
            
            # Total de places disponibles
            from django.db.models import Sum
            total_places = Trajet.objects.filter(
                statut='actif',
                date_depart__gte=timezone.now()
            ).aggregate(Sum('places_disponibles'))['places_disponibles__sum'] or 0
            
            # Derniers trajets actifs
            derniers_trajets = Trajet.objects.filter(
                statut='actif',
                date_depart__gte=timezone.now()
            ).order_by('-date_depart')[:5]
            
            return Response({
                'status': 'success',
                'data': {
                    'total_trajets_actifs': total_trajets,
                    'total_trajets': total_trajets_tous,
                    'trajets_aujourd_hui': trajets_aujourd_hui,
                    'trajets_disponibles': trajets_disponibles,
                    'total_places_disponibles': int(total_places),
                    'derniers_trajets': TrajetSerializer(derniers_trajets, many=True).data
                }
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StatistiquesTransporteurView(APIView):
    """Statistiques pour un transporteur"""
    permission_classes = [IsTransporteur]
    
    def get(self, request):
        try:
            transporteur = request.user.transporteur_profile
            
            # Statistiques des trajets
            total_trajets = Trajet.objects.filter(transporteur=transporteur).count()
            trajets_actifs = Trajet.objects.filter(
                transporteur=transporteur,
                statut='actif'
            ).count()
            trajets_termines = Trajet.objects.filter(
                transporteur=transporteur,
                statut='termine'
            ).count()
            
            # Total de places
            from django.db.models import Sum
            total_places = Trajet.objects.filter(
                transporteur=transporteur
            ).aggregate(Sum('places_totales'))['places_totales__sum'] or 0
            
            places_reservees = Trajet.objects.filter(
                transporteur=transporteur
            ).aggregate(Sum('places_reservees'))['places_reserved__sum'] or 0
            
            # Taux de remplissage moyen
            from django.db.models import Avg
            taux_moyen = Trajet.objects.filter(
                transporteur=transporteur
            ).aggregate(Avg('places_reserved'))['places_reserved__avg'] or 0
            
            # Total de réservations
            from reservations.models import Reservation
            total_reservations = Reservation.objects.filter(
                trajet__transporteur=transporteur
            ).count()
            
            return Response({
                'status': 'success',
                'data': {
                    'total_trajets': total_trajets,
                    'trajets_actifs': trajets_actifs,
                    'trajets_termines': trajets_termines,
                    'total_places': int(total_places),
                    'places_reservees': int(places_reservees),
                    'taux_remplissage_moyen': round(taux_moyen, 2),
                    'total_reservations': total_reservations
                }
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )