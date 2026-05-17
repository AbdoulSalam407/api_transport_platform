from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Count, Q, F
from .models import Trajet, Etape
from .serializers import (
    TrajetSerializer,
    TrajetBriefSerializer,
    EtapeSerializer,
    RechercheTrajetSerializer,
)
from core.permissions import IsAdmin, IsTransporteur, IsAdminOrTransporteur
from core.validation import VALIDATION_APPROUVE, VALIDATION_EN_ATTENTE


def queryset_trajets_visibles_passagers():
    """Trajets réservables par un passager (approuvés, actifs, places libres)."""
    return Trajet.objects.filter(
        validation_statut=VALIDATION_APPROUVE,
        statut='actif',
        date_depart__gte=timezone.now(),
        places_disponibles__gt=0,
    )


def queryset_trajets_liste_plateforme():
    """Tous les trajets disponibles sur la plateforme (consultation, y compris complets)."""
    return Trajet.objects.filter(
        validation_statut=VALIDATION_APPROUVE,
        statut='actif',
        date_depart__gte=timezone.now(),
    ).select_related('transporteur', 'vehicule').order_by('date_depart')


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
        user = self.request.user
        if user.is_authenticated and getattr(user, 'role', None) == 'admin':
            queryset = Trajet.objects.all().order_by('-date_depart')
        elif user.is_authenticated and getattr(user, 'role', None) == 'transporteur':
            queryset = Trajet.objects.filter(
                transporteur__utilisateur=user
            ).order_by('-date_depart')
        else:
            queryset = queryset_trajets_visibles_passagers()
        
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
        user = self.request.user
        if user.role == 'admin':
            serializer.save(
                validation_statut=VALIDATION_APPROUVE,
                valide_par=user,
                date_validation=timezone.now(),
            )
        else:
            transporteur = user.transporteur_profile
            vehicule = serializer.validated_data.get('vehicule')
            if vehicule and not serializer.validated_data.get('places_totales'):
                serializer.validated_data['places_totales'] = vehicule.capacite_places
            if serializer.validated_data.get('places_disponibles', 0) == 0:
                serializer.validated_data['places_disponibles'] = serializer.validated_data[
                    'places_totales'
                ]
            serializer.save(transporteur=transporteur, validation_statut=VALIDATION_EN_ATTENTE)


class EtapeViewSet(viewsets.ModelViewSet):
    """CRUD pour les étapes"""
    queryset = Etape.objects.all()
    serializer_class = EtapeSerializer
    permission_classes = [IsAdminOrTransporteur]


class RechercherTrajetView(generics.ListAPIView):
    """Lister / filtrer les trajets disponibles sur la plateforme."""
    serializer_class = TrajetSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        reservable_only = self.request.query_params.get(
            'reservable_only', 'false'
        ).lower() == 'true'
        queryset = (
            queryset_trajets_visibles_passagers()
            if reservable_only
            else queryset_trajets_liste_plateforme()
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
            trajet = Trajet.objects.get(
                id=pk,
                validation_statut=VALIDATION_APPROUVE,
                statut='actif',
            )
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
    serializer_class = TrajetBriefSerializer
    permission_classes = [IsTransporteur]
    pagination_class = StandardPagination
    
    def get_queryset(self):
        transporteur = self.request.user.transporteur_profile
        queryset = Trajet.objects.filter(
            transporteur=transporteur
        ).select_related('transporteur', 'vehicule').order_by('-date_depart')
        
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
    """Statistiques globales pour la home page (page d'accueil publique)."""
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        try:
            # Statistiques de base
            total_trajets = queryset_trajets_visibles_passagers().count()
            
            total_trajets_tous = Trajet.objects.all().count()
            trajets_aujourd_hui = Trajet.objects.filter(
                date_depart__date=timezone.now().date()
            ).count()
            
            # Trajets avec places disponibles
            trajets_disponibles = queryset_trajets_visibles_passagers().count()
            
            # Total de places disponibles
            from django.db.models import Sum
            total_places = queryset_trajets_visibles_passagers().aggregate(
                Sum('places_disponibles')
            )['places_disponibles__sum'] or 0
            
            # Derniers trajets actifs (approuvés)
            derniers_trajets = queryset_trajets_visibles_passagers().order_by('-date_depart')[:5]
            
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
            from django.db.models import Sum, Count, Q
            from reservations.models import Reservation
            from core.validation import VALIDATION_EN_ATTENTE, VALIDATION_APPROUVE

            transporteur = request.user.transporteur_profile
            qs = Trajet.objects.filter(transporteur=transporteur)

            total_trajets = qs.count()
            trajets_actifs = qs.filter(statut='actif').count()
            trajets_termines = qs.filter(statut='termine').count()
            trajets_en_attente = qs.filter(validation_statut=VALIDATION_EN_ATTENTE).count()
            trajets_approuves = qs.filter(validation_statut=VALIDATION_APPROUVE).count()

            agg = qs.aggregate(
                total_places=Sum('places_totales'),
                places_disponibles=Sum('places_disponibles'),
            )
            total_places = int(agg['total_places'] or 0)
            places_disponibles = int(agg['places_disponibles'] or 0)
            places_reservees = max(0, total_places - places_disponibles)

            if total_places > 0:
                taux_remplissage = round((places_reservees / total_places) * 100, 1)
            else:
                taux_remplissage = 0.0

            total_reservations = Reservation.objects.filter(
                trajet__transporteur=transporteur
            ).count()
            reservations_confirmees = Reservation.objects.filter(
                trajet__transporteur=transporteur,
                statut='confirmee',
            ).count()
            reservations_en_attente = Reservation.objects.filter(
                trajet__transporteur=transporteur,
                statut='en_attente',
            ).count()
            
            return Response({
                'status': 'success',
                'data': {
                    'total_trajets': total_trajets,
                    'trajets_actifs': trajets_actifs,
                    'trajets_termines': trajets_termines,
                    'trajets_en_attente': trajets_en_attente,
                    'trajets_approuves': trajets_approuves,
                    'total_places': total_places,
                    'places_reservees': places_reservees,
                    'places_disponibles': places_disponibles,
                    'taux_remplissage_moyen': taux_remplissage,
                    'total_reservations': total_reservations,
                    'reservations_confirmees': reservations_confirmees,
                    'reservations_en_attente': reservations_en_attente,
                }
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TrajetsEnAttenteAdminView(generics.ListAPIView):
    """Liste des trajets en attente de validation (admin)."""
    serializer_class = TrajetSerializer
    permission_classes = [IsAdmin]
    pagination_class = StandardPagination

    def get_queryset(self):
        return Trajet.objects.filter(
            validation_statut=VALIDATION_EN_ATTENTE
        ).select_related('transporteur', 'transporteur__utilisateur').order_by('date_creation')


class ApprouverTrajetAdminView(APIView):
    """Approuver un trajet (admin)."""
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            trajet = Trajet.objects.get(pk=pk)
            if trajet.validation_statut == VALIDATION_APPROUVE:
                return Response({'message': 'Ce trajet est déjà approuvé.'})
            trajet.approuver(request.user)
            return Response({
                'message': 'Trajet approuvé. Il est maintenant visible pour les passagers.',
                'trajet': TrajetSerializer(trajet).data,
            })
        except Trajet.DoesNotExist:
            return Response({'error': 'Trajet non trouvé'}, status=status.HTTP_404_NOT_FOUND)


class RejeterTrajetAdminView(APIView):
    """Rejeter un trajet (admin)."""
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            trajet = Trajet.objects.get(pk=pk)
            motif = request.data.get('motif', '')
            trajet.rejeter(request.user, motif=motif)
            return Response({
                'message': 'Trajet rejeté.',
                'trajet': TrajetSerializer(trajet).data,
            })
        except Trajet.DoesNotExist:
            return Response({'error': 'Trajet non trouvé'}, status=status.HTTP_404_NOT_FOUND)