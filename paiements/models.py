from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Paiement(models.Model):
    """Modèle pour les paiements"""
    
    METHODE_CHOICES = [
        ("carte_bancaire", "Carte bancaire"),
        ("mobile_money", "Mobile Money"),
        ("virement", "Virement"),
        ("especes", "Espèces"),
        ("portefeuille", "Portefeuille numérique"),
    ]
    
    STATUS_CHOICES = [
        ("en_attente", "En attente"),
        ("traitement", "En traitement"),
        ("reussi", "Réussi"),
        ("echoue", "Échoué"),
        ("rembourse", "Remboursé"),
    ]
    
    reservation = models.OneToOneField(
        "reservations.Reservation",
        on_delete=models.CASCADE,
        related_name="paiement",
        verbose_name="Réservation"
    )
    client = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="paiements",
        verbose_name="Client"
    )
    
    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Montant"
    )
    methode_paiement = models.CharField(
        max_length=20,
        choices=METHODE_CHOICES,
        verbose_name="Méthode de paiement"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="en_attente",
        verbose_name="Statut"
    )
    
    reference_transaction = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Référence de transaction"
    )
    reference_externe = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Référence externe (gateway)"
    )
    
    date_paiement = models.DateTimeField(auto_now_add=True)
    date_confirmation = models.DateTimeField(null=True, blank=True)
    date_remboursement = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        ordering = ["-date_paiement"]
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
    
    def __str__(self):
        return f"Paiement {self.reference_transaction} - {self.montant} ({self.status})"
