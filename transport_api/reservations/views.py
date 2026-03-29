from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Role

from .models import Reservation, ReservationStatut
from .serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        qs = Reservation.objects.select_related("passager", "trajet").all()
        user = self.request.user
        if user.role == Role.PASSAGER:
            return qs.filter(passager=user.passager_profile)
        if user.role == Role.TRANSPORTEUR:
            return qs.filter(trajet__transporteur=user.transporteur_profile)
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != Role.PASSAGER:
            raise permissions.PermissionDenied("Seuls les passagers créent des réservations.")
        serializer.save(passager=user.passager_profile)

    @action(detail=True, methods=["post"], url_path="annuler")
    def annuler(self, request, pk=None):
        reservation = self.get_object()
        if request.user.role == Role.PASSAGER and reservation.passager_id != request.user.passager_profile.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        ser = ReservationSerializer(
            reservation,
            data={"statut": ReservationStatut.ANNULE},
            partial=True,
        )
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)
