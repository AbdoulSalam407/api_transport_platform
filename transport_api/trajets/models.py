from django.db import models

from users.models import Transporteur
from vehicules.models import Vehicule


class TrajetStatut(models.TextChoices):
    PLANIFIE = "planifie", "Planifié"
    OUVERT = "ouvert", "Ouvert aux réservations"
    COMPLET = "complet", "Complet"
    ANNULE = "annule", "Annulé"
    TERMINE = "termine", "Terminé"


class Trajet(models.Model):
    ville_depart = models.CharField(max_length=150)
    ville_arrivee = models.CharField(max_length=150)
    date_depart = models.DateField()
    heure_depart = models.TimeField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_places_disponibles = models.PositiveIntegerField()
    statut = models.CharField(
        max_length=20,
        choices=TrajetStatut.choices,
        default=TrajetStatut.OUVERT,
    )
    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.PROTECT,
        related_name="trajets",
    )
    transporteur = models.ForeignKey(
        Transporteur,
        on_delete=models.CASCADE,
        related_name="trajets",
    )

    class Meta:
        ordering = ["date_depart", "heure_depart"]

    def __str__(self):
        return f"{self.ville_depart} → {self.ville_arrivee} ({self.date_depart})"
