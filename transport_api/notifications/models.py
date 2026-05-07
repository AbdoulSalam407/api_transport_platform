from django.conf import settings
from django.db import models
from django.utils import timezone


class NotificationType(models.TextChoices):
    RESERVATION = "reservation", "Réservation"
    PAIEMENT = "paiement", "Paiement"
    SYSTEME = "systeme", "Système"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    message = models.TextField()
    type = models.CharField(max_length=30, choices=NotificationType.choices)
    date_envoi = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date_envoi"]

    def __str__(self):
        return f"{self.type} → {self.user.email}"
