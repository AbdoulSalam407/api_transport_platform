from django.db import transaction
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from notifications.services import notify_payment_validated
from reservations.models import ReservationStatut
from reservations.serializers import ReservationSerializer
from users.models import Role

from .models import Paiement, PaiementStatut
from .serializers import PaiementSerializer


class PaiementViewSet(viewsets.ModelViewSet):
    serializer_class = PaiementSerializer

    def get_queryset(self):
        qs = Paiement.objects.select_related("reservation__trajet", "reservation__passager").all()
        user = self.request.user
        if user.role == Role.PASSAGER:
            return qs.filter(reservation__passager=user.passager_profile)
        return qs

    def perform_create(self, serializer):
        res = serializer.validated_data["reservation"]
        if self.request.user.role != Role.PASSAGER:
            raise permissions.PermissionDenied()
        if res.passager_id != self.request.user.passager_profile.pk:
            raise permissions.PermissionDenied("Réservation invalide.")
        serializer.save()

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def valider(self, request, pk=None):
        """Valide un paiement (réservé au staff / admin)."""

        with transaction.atomic():
            paiement = (
                Paiement.objects.select_for_update()
                .select_related("reservation", "reservation__trajet")
                .get(pk=pk)
            )
            if paiement.statut == PaiementStatut.VALIDE:
                return Response(PaiementSerializer(paiement).data)
            paiement.statut = PaiementStatut.VALIDE
            paiement.save(update_fields=["statut"])
            reservation = paiement.reservation
            if reservation.statut == ReservationStatut.EN_ATTENTE:
                ser = ReservationSerializer(
                    reservation,
                    data={"statut": ReservationStatut.CONFIRME},
                    partial=True,
                )
                ser.is_valid(raise_exception=True)
                ser.save()
            notify_payment_validated(paiement)
        return Response(PaiementSerializer(paiement).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def marquer_valide(self, request, pk=None):
        """
        Démo : marque un paiement comme validé et confirme la réservation.
        En production, brancher sur un webhook PSP et sécuriser cet endpoint.
        """
        with transaction.atomic():
            paiement = (
                Paiement.objects.select_for_update()
                .select_related("reservation", "reservation__trajet")
                .get(pk=pk)
            )
            if paiement.reservation.passager.user_id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)
            if paiement.statut != PaiementStatut.EN_ATTENTE:
                return Response(
                    {"detail": "Paiement déjà traité."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            paiement.statut = PaiementStatut.VALIDE
            paiement.save(update_fields=["statut"])
            reservation = paiement.reservation
            if reservation.statut == ReservationStatut.EN_ATTENTE:
                ser = ReservationSerializer(
                    reservation,
                    data={"statut": ReservationStatut.CONFIRME},
                    partial=True,
                )
                ser.is_valid(raise_exception=True)
                ser.save()
            notify_payment_validated(paiement)
        return Response(PaiementSerializer(paiement).data)
