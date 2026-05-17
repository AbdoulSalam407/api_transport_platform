from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.utils import timezone
from .models import Reservation, Billet, PointRamassage
from .serializers import (
    ReservationSerializer, ReservationListSerializer, ReservationCreateSerializer,
    BilletSerializer, PointRamassageSerializer
)
from core.permissions import IsAdmin, IsPassager, IsTransporteur, IsAdminOrSelf
from rest_framework.exceptions import PermissionDenied
import qrcode

from io import BytesIO
import uuid


# ==================== PAGINATION ====================
class StandardPagination(PageNumberPagination):
    """Pagination standardisée pour tous les endpoints"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReservationViewSet(viewsets.ModelViewSet):
    """CRUD pour les réservations - AVEC PAGINATION"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = StandardPagination
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsPassager()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminOrSelf()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'admin':
            return Reservation.objects.all().order_by('-date_reservation')
        elif user.role == 'passager':
            return Reservation.objects.filter(passager__utilisateur=user).order_by('-date_reservation')
        elif user.role == 'transporteur':
            return Reservation.objects.filter(trajet__transporteur__utilisateur=user).order_by('-date_reservation')
        
        return Reservation.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.role != 'passager':
            raise PermissionDenied('Seuls les passagers peuvent créer une réservation.')
        passager = self.request.user.passager_profile
        serializer.save(passager=passager)


class CreerReservationView(APIView):
    """Créer une nouvelle réservation"""
    permission_classes = [IsPassager]
    
    @transaction.atomic
    def post(self, request):
        serializer = ReservationCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        reservation = serializer.save()

        sieges = reservation.sieges_affichage
        detail_sieges = f' {sieges}.' if sieges else ''
        return Response(
            {
                'message': (
                    f'Réservation enregistrée.{detail_sieges} '
                    f'Validation par un administrateur requise.'
                ),
                'reservation': ReservationSerializer(reservation).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ConfirmerReservationView(APIView):
    """Confirmer une réservation (admin uniquement)."""
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        try:
            reservation = Reservation.objects.get(id=pk)
            
            if reservation.statut != 'en_attente':
                return Response(
                    {'error': 'Cette réservation ne peut plus être confirmée.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if reservation.trajet.validation_statut != 'approuve':
                return Response(
                    {'error': 'Le trajet associé doit être approuvé par l\'admin.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if reservation.confirmer():
                from notifications.services import notifier_reservation_confirmee
                notifier_reservation_confirmee(reservation)
                return Response({
                    'message': 'Réservation confirmée par l\'administrateur.',
                    'reservation': ReservationSerializer(reservation).data,
                })
            return Response(
                {'error': 'Impossible de confirmer - plus de places disponibles'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Reservation.DoesNotExist:
            return Response(
                {'error': 'Réservation non trouvée'},
                status=status.HTTP_404_NOT_FOUND,
            )


class ReservationsEnAttenteAdminView(generics.ListAPIView):
    """Réservations en attente de validation admin."""
    serializer_class = ReservationSerializer
    permission_classes = [IsAdmin]
    pagination_class = StandardPagination

    def get_queryset(self):
        return Reservation.objects.filter(statut='en_attente').select_related(
            'passager', 'passager__utilisateur', 'trajet'
        ).order_by('-date_reservation')


class AnnulerReservationView(APIView):
    """Annuler une réservation"""
    permission_classes = [IsPassager]
    
    def post(self, request, pk):
        try:
            reservation = Reservation.objects.get(
                id=pk,
                passager__utilisateur=request.user
            )
            
            if reservation.annuler():
                return Response({
                    'message': 'Réservation annulée',
                    'reservation': ReservationSerializer(reservation).data
                })
            else:
                return Response(
                    {'error': 'Impossible d\'annuler cette réservation'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Reservation.DoesNotExist:
            return Response(
                {'error': 'Réservation non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )


class MarquerRecupereView(APIView):
    """Marquer un passager comme récupéré"""
    permission_classes = [IsTransporteur]
    
    def post(self, request, pk):
        try:
            reservation = Reservation.objects.get(
                id=pk,
                trajet__transporteur__utilisateur=request.user
            )
            
            if reservation.marquer_recupere():
                return Response({'message': 'Passager marqué comme récupéré'})
            else:
                return Response(
                    {'error': 'Impossible de marquer comme récupéré'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Reservation.DoesNotExist:
            return Response(
                {'error': 'Réservation non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )


class MesReservationsView(generics.ListAPIView):
    """Lister mes réservations (passager) - AVEC PAGINATION"""
    serializer_class = ReservationListSerializer
    permission_classes = [IsPassager]
    pagination_class = StandardPagination
    
    def get_queryset(self):
        queryset = Reservation.objects.filter(
            passager__utilisateur=self.request.user
        ).select_related('trajet', 'passager').order_by('-date_reservation')
        
        # Filtrer par statut si fourni
        statut = self.request.query_params.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        return queryset


class BilletViewSet(viewsets.ModelViewSet):
    """CRUD pour les billets"""
    queryset = Billet.objects.all()
    serializer_class = BilletSerializer
    permission_classes = [IsPassager]
    
    def get_queryset(self):
        return Billet.objects.filter(
            reservation__passager__utilisateur=self.request.user
        )


class GenererBilletView(APIView):
    """Générer un billet électronique"""
    permission_classes = [IsPassager]
    
    @transaction.atomic
    def post(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(
                id=reservation_id,
                passager__utilisateur=request.user,
                statut='confirmee'
            )
            
            # Vérifier si un billet existe déjà
            if hasattr(reservation, 'billet'):
                return Response(
                    BilletSerializer(reservation.billet).data,
                    status=status.HTTP_200_OK
                )
            
            # Générer un code QR unique
            qr_code = str(uuid.uuid4()).replace('-', '')[:20]
            
            # Créer le billet
            billet = Billet.objects.create(
                reservation=reservation,
                code_qr=qr_code
            )
            
            return Response(
                BilletSerializer(billet, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
            
        except Reservation.DoesNotExist:
            return Response(
                {'error': 'Réservation non trouvée ou non confirmée'},
                status=status.HTTP_404_NOT_FOUND
            )


class GenererQRCodeView(APIView):
    """Générer l'image du QR code"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, code_qr):
        try:
            billet = Billet.objects.get(code_qr=code_qr)
            
            # Vérifier l'accès
            user = request.user
            if not (user.role == 'admin' or
                    billet.reservation.passager.utilisateur == user or
                    billet.reservation.trajet.transporteur.utilisateur == user):
                return Response(
                    {'error': 'Accès non autorisé'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Générer le QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"BILLET:{billet.code_qr}:{billet.reservation.id}")
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convertir en réponse HTTP
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            from django.http import HttpResponse
            return HttpResponse(buffer.getvalue(), content_type="image/png")
            
        except Billet.DoesNotExist:
            return Response(
                {'error': 'Billet non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )


class PointRamassageViewSet(viewsets.ModelViewSet):
    """CRUD pour les points de ramassage"""
    queryset = PointRamassage.objects.all()
    serializer_class = PointRamassageSerializer
    permission_classes = [IsPassager]
    
    def get_queryset(self):
        return PointRamassage.objects.filter(
            reservation__passager__utilisateur=self.request.user
        )
    
    def perform_create(self, serializer):
        reservation_id = self.request.data.get('reservation')
        reservation = Reservation.objects.get(
            id=reservation_id,
            passager__utilisateur=self.request.user
        )
        serializer.save(reservation=reservation)


class DefinirPointRamassageView(APIView):
    """Définir un point de ramassage"""
    permission_classes = [IsPassager]
    
    def post(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(
                id=reservation_id,
                passager__utilisateur=request.user
            )
            
            serializer = PointRamassageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(reservation=reservation)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Reservation.DoesNotExist:
            return Response(
                {'error': 'Réservation non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )