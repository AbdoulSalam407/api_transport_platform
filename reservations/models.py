from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Reservation(models.Model):
    """Modèle pour les réservations"""
    
    STATUS_CHOICES = [
        ("en_attente", "En attente"),
        ("confirmee", "Confirmée"),
        ("payee", "Payée"),
        ("en_cours", "En cours"),
        ("terminee", "Terminée"),
        ("annulee", "Annulée"),
    ]
    
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations",
        limit_choices_to={"role": "client"},
        verbose_name="Client"
    )
    trajet = models.ForeignKey(
        "trajets.Trajet",
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Trajet"
    )
    
    nombre_places = models.PositiveIntegerField(
        default=1,
        verbose_name="Nombre de places"
    )
    prix_total = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Prix total"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="en_attente",
        verbose_name="Statut"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )
    
    date_reservation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_annulation = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ["-date_reservation"]
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        unique_together = ["client", "trajet"]
    
    def __str__(self):
        return f"Réservation {self.id} - {self.client} - {self.trajet}"
