from django.db import models
from users.models import CustomUser
from reservations.models import Reservation


class Notification(models.Model):
    """Modèle pour les notifications"""
    
    TYPE_CHOICES = [
        ('reservation', 'Réservation'),
        ('rappel', 'Rappel'),
        ('depart_imminent', 'Départ imminent'),
        ('annulation', 'Annulation'),
        ('modification', 'Modification'),
        ('promotion', 'Promotion'),
        ('systeme', 'Système'),
    ]
    
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)
    
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    est_lu = models.BooleanField(default=False)
    data = models.JSONField(default=dict, blank=True)  # Données supplémentaires
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.titre} - {self.utilisateur}"
    
    def marquer_lue(self):
        """Marquer la notification comme lue"""
        from django.utils import timezone
        self.est_lu = True
        self.date_lecture = timezone.now()
        self.save()