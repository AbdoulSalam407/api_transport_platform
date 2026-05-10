from django.db import transaction
from rest_framework import serializers

from trajets.models import Trajet, TrajetStatut

from .models import Reservation, ReservationStatut


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            "id",
            "passager",
            "trajet",
            "nombre_places",
            "date_reservation",
            "statut",
        )
        read_only_fields = ("date_reservation", "passager")

    def validate(self, attrs):
        trajet: Trajet = attrs.get("trajet") or getattr(self.instance, "trajet", None)
        nombre = attrs.get("nombre_places")
        if self.instance:
            nombre = nombre if nombre is not None else self.instance.nombre_places
        next_statut = attrs.get("statut", getattr(self.instance, "statut", None))
        if next_statut == ReservationStatut.ANNULE:
            return attrs
        if trajet and nombre:
            if trajet.statut in (TrajetStatut.ANNULE, TrajetStatut.TERMINE):
                raise serializers.ValidationError("Ce trajet n'accepte pas de réservation.")
            bloque_complet = trajet.statut == TrajetStatut.COMPLET and not (
                self.instance
                and self.instance.statut == ReservationStatut.CONFIRME
                and self.instance.trajet_id == trajet.pk
            )
            if bloque_complet:
                raise serializers.ValidationError("Ce trajet n'accepte pas de réservation.")
            if trajet.nombre_places_disponibles < nombre:
                raise serializers.ValidationError("Pas assez de places disponibles sur ce trajet.")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        trajet = Trajet.objects.select_for_update().get(pk=validated_data["trajet"].pk)
        nombre = validated_data["nombre_places"]
        statut = validated_data.get("statut", ReservationStatut.EN_ATTENTE)
        if trajet.nombre_places_disponibles < nombre:
            raise serializers.ValidationError({"nombre_places": "Places insuffisantes."})
        if statut == ReservationStatut.CONFIRME:
            trajet.nombre_places_disponibles -= nombre
            if trajet.nombre_places_disponibles == 0:
                trajet.statut = TrajetStatut.COMPLET
            trajet.save(update_fields=["nombre_places_disponibles", "statut"])
        return Reservation.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        ancien_nombre = instance.nombre_places
        ancien_statut = instance.statut
        nouveau_statut = validated_data.get("statut", instance.statut)
        nouveau_nombre = validated_data.get("nombre_places", instance.nombre_places)

        trajet = Trajet.objects.select_for_update().get(pk=instance.trajet_id)

        # Annulation : libère les places si la réservation était confirmée
        if (
            nouveau_statut == ReservationStatut.ANNULE
            and ancien_statut == ReservationStatut.CONFIRME
        ):
            trajet.nombre_places_disponibles += ancien_nombre
            if trajet.statut == TrajetStatut.COMPLET:
                trajet.statut = TrajetStatut.OUVERT
            trajet.save(update_fields=["nombre_places_disponibles", "statut"])

        # Passage en confirmé depuis en_attente
        if (
            nouveau_statut == ReservationStatut.CONFIRME
            and ancien_statut == ReservationStatut.EN_ATTENTE
        ):
            if trajet.nombre_places_disponibles < nouveau_nombre:
                raise serializers.ValidationError("Pas assez de places pour confirmer.")
            trajet.nombre_places_disponibles -= nouveau_nombre
            if trajet.nombre_places_disponibles == 0:
                trajet.statut = TrajetStatut.COMPLET
            trajet.save(update_fields=["nombre_places_disponibles", "statut"])

        # Mise à jour du nombre de places si déjà confirmé
        if (
            nouveau_statut == ReservationStatut.CONFIRME
            and ancien_statut == ReservationStatut.CONFIRME
            and nouveau_nombre != ancien_nombre
        ):
            delta = nouveau_nombre - ancien_nombre
            if delta > 0 and trajet.nombre_places_disponibles < delta:
                raise serializers.ValidationError("Pas assez de places.")
            trajet.nombre_places_disponibles -= delta
            if trajet.nombre_places_disponibles == 0:
                trajet.statut = TrajetStatut.COMPLET
            elif trajet.statut == TrajetStatut.COMPLET and trajet.nombre_places_disponibles > 0:
                trajet.statut = TrajetStatut.OUVERT
            trajet.save(update_fields=["nombre_places_disponibles", "statut"])

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance
