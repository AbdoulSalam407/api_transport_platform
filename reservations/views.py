from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des réservations"""
    
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status"]
    ordering_fields = ["date_reservation", "prix_total"]
    
    def get_queryset(self):
        """Retourner les réservations de l'utilisateur connecté"""
        user = self.request.user
        if user.is_staff or user.role == "admin":
            return Reservation.objects.all()
        return Reservation.objects.filter(client=user)
    
    def perform_create(self, serializer):
        """Créer une réservation pour l'utilisateur connecté"""
        serializer.save(client=self.request.user)
    
    @action(detail=True, methods=["post"])
    def annuler(self, request, pk=None):
        """Annuler une réservation"""
        from django.utils import timezone
        
        reservation = self.get_object()
        if reservation.status in ["terminee", "annulee"]:
            return Response(
                {"error": "Impossible d'annuler cette réservation"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.status = "annulee"
        reservation.date_annulation = timezone.now()
        reservation.save()
        
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)
