from rest_framework import permissions, viewsets

from users.models import Role

from .models import Trajet
from .serializers import TrajetSerializer


class TrajetViewSet(viewsets.ModelViewSet):
    serializer_class = TrajetSerializer

    def get_queryset(self):
        qs = Trajet.objects.select_related("vehicule", "transporteur").all()
        p = self.request.query_params
        vd = p.get("ville_depart")
        va = p.get("ville_arrivee")
        dd = p.get("date_depart")
        st = p.get("statut")
        if vd:
            qs = qs.filter(ville_depart__icontains=vd)
        if va:
            qs = qs.filter(ville_arrivee__icontains=va)
        if dd:
            qs = qs.filter(date_depart=dd)
        if st:
            qs = qs.filter(statut=st)
        ordering = p.get("ordering", "date_depart")
        if ordering.lstrip("-") in ("date_depart", "heure_depart", "prix"):
            qs = qs.order_by(ordering)
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != Role.TRANSPORTEUR:
            raise permissions.PermissionDenied("Seuls les transporteurs créent des trajets.")
        vehicule_id = serializer.validated_data.get("vehicule").pk
        if not user.transporteur_profile.vehicules.filter(pk=vehicule_id).exists():
            raise permissions.PermissionDenied("Véhicule invalide pour ce transporteur.")
        serializer.save(transporteur=user.transporteur_profile)

    def perform_update(self, serializer):
        trajet = self.get_object()
        if self.request.user.role != Role.TRANSPORTEUR:
            raise permissions.PermissionDenied()
        if trajet.transporteur_id != self.request.user.transporteur_profile.pk:
            raise permissions.PermissionDenied()
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != Role.TRANSPORTEUR:
            raise permissions.PermissionDenied()
        if instance.transporteur_id != self.request.user.transporteur_profile.pk:
            raise permissions.PermissionDenied()
        instance.delete()
