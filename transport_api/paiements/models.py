from django.db import models
from django.utils import timezone

from reservations.models import Reservation


class MethodePaiement(models.TextChoices):
    CARTE = "carte", "Carte"
    ESPECES = "especes", "Espèces"
    MOBILE_MONEY = "mobile_money", "Mobile money"
    VIREMENT = "virement", "Virement"


class PaiementStatut(models.TextChoices):
    EN_ATTENTE = "en_attente", "En attente"
    VALIDE = "valide", "Validé"
    ECHOUE = "echoue", "Échoué"
    REMBOURSE = "rembourse", "Remboursé"


class Paiement(models.Model):
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="paiements",
    )
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    methode = models.CharField(max_length=20, choices=MethodePaiement.choices)
    statut = models.CharField(
        max_length=20,
        choices=PaiementStatut.choices,
        default=PaiementStatut.EN_ATTENTE,
    )
    date_paiement = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date_paiement"]

    def __str__(self):
        return f"Paiement {self.pk} — {self.montant} ({self.statut})"
