from django.db import models
from django.utils import timezone

from trajets.models import Trajet
from users.models import Passager


class ReservationStatut(models.TextChoices):
    EN_ATTENTE = "en_attente", "En attente"
    CONFIRME = "confirme", "Confirmé"
    ANNULE = "annule", "Annulé"


class Reservation(models.Model):
    passager = models.ForeignKey(
        Passager,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    trajet = models.ForeignKey(
        Trajet,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    nombre_places = models.PositiveIntegerField(default=1)
    date_reservation = models.DateTimeField(default=timezone.now)
    statut = models.CharField(
        max_length=20,
        choices=ReservationStatut.choices,
        default=ReservationStatut.EN_ATTENTE,
    )

    class Meta:
        ordering = ["-date_reservation"]

    def __str__(self):
        return f"Réservation {self.pk} — {self.passager_id}"
