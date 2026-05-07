from django.db import models

from users.models import Transporteur


class TypeVehicule(models.TextChoices):
    BUS = "BUS", "Bus"
    MINIBUS = "MINIBUS", "Minibus"
    VAN = "VAN", "Van"
    BERLINE = "BERLINE", "Berline"


class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=32, unique=True)
    capacite = models.PositiveIntegerField()
    type = models.CharField(max_length=20, choices=TypeVehicule.choices)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    transporteur = models.ForeignKey(
        Transporteur,
        on_delete=models.CASCADE,
        related_name="vehicules",
    )

    def __str__(self):
        return f"{self.immatriculation} ({self.type})"
