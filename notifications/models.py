from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    """Modèle pour les notifications"""
    
    TYPE_CHOICES = [
        ("reservation", "Réservation"),
        ("paiement", "Paiement"),
        ("trajet", "Trajet"),
        ("annulation", "Annulation"),
        ("alerte", "Alerte"),
        ("info", "Information"),
    ]
    
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Utilisateur"
    )
    
    titre = models.CharField(max_length=200, verbose_name="Titre")
    message = models.TextField(verbose_name="Message")
    type_notification = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type"
    )
    
    is_read = models.BooleanField(
        default=False,
        verbose_name="Lue"
    )
    
    lien = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Lien"
    )
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        indexes = [
            models.Index(fields=["-date_creation"]),
            models.Index(fields=["utilisateur", "is_read"]),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.utilisateur}"
