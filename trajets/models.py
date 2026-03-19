from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Trajet(models.Model):
    """Modèle pour les trajets planifiés"""
    
    STATUS_CHOICES = [
        ("planifie", "Planifié"),
        ("en_cours", "En cours"),
        ("termine", "Terminé"),
        ("annule", "Annulé"),
    ]
    
    vehicule = models.ForeignKey(
        "vehicules.Vehicule",
        on_delete=models.CASCADE,
        related_name="trajets",
        verbose_name="Véhicule"
    )
    chauffeur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": "driver"},
        related_name="trajets",
        verbose_name="Chauffeur"
    )
    
    depart = models.CharField(max_length=100, verbose_name="Point de départ")
    arrivee = models.CharField(max_length=100, verbose_name="Point d'arrivée")
    distance_km = models.FloatField(verbose_name="Distance (km)")
    duree_estimee = models.DurationField(verbose_name="Durée estimée")
    
    date_depart = models.DateTimeField(verbose_name="Date/Heure de départ")
    date_arrivee_estimee = models.DateTimeField(verbose_name="Date/Heure d'arrivée estimée", null=True, blank=True)
    date_arrivee_reelle = models.DateTimeField(verbose_name="Date/Heure d'arrivée réelle", null=True, blank=True)
    
    prix_base = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Prix de base"
    )
    places_disponibles = models.PositiveIntegerField(verbose_name="Places disponibles")
    places_totales = models.PositiveIntegerField(verbose_name="Places totales")
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planifie",
        verbose_name="Statut"
    )
    
    points_arret = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Points d'arrêt"
    )
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["date_depart"]
        verbose_name = "Trajet"
        verbose_name_plural = "Trajets"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["date_depart"]),
        ]
    
    def __str__(self):
        return f"{self.depart} → {self.arrivee} ({self.date_depart.strftime('%d/%m/%Y %H:%M')})"
