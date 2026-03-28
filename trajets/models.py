from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Trajet(models.Model):
    """Modèle pour les trajets planifiés"""
    
    STATUT_CHOICES = [
        ("planifie", "Planifié"),
        ("en_cours", "En cours"),
        ("termine", "Terminé"),
        ("annule", "Annulé"),
    ]
    
    # Relations
    vehicule = models.ForeignKey(
        "vehicules.Vehicule",
        on_delete=models.CASCADE,
        related_name="trajets",
        verbose_name="Véhicule"
    )
    transporteur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": "driver"},
        related_name="trajets_transporteur",
        verbose_name="Transporteur"
    )
    
    # Localisation
    ville_depart = models.CharField(max_length=100, verbose_name="Ville de départ")
    ville_arrivee = models.CharField(max_length=100, verbose_name="Ville d'arrivée")
    distance_km = models.FloatField(verbose_name="Distance (km)")
    duree_estimee = models.DurationField(verbose_name="Durée estimée")
    
    # Dates et heures
    date_depart = models.DateField(verbose_name="Date de départ")
    heure_depart = models.TimeField(verbose_name="Heure de départ")
    date_arrivee_estimee = models.DateTimeField(verbose_name="Date/Heure d'arrivée estimée", null=True, blank=True)
    date_arrivee_reelle = models.DateTimeField(verbose_name="Date/Heure d'arrivée réelle", null=True, blank=True)
    
    # Tarification et places
    prix = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Prix"
    )
    nombre_places_disponibles = models.PositiveIntegerField(verbose_name="Nombre de places disponibles")
    places_totales = models.PositiveIntegerField(verbose_name="Places totales")
    
    # Statut
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="planifie",
        verbose_name="Statut"
    )
    
    # Informations supplémentaires
    points_arret = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Points d'arrêt"
    )
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-date_depart"]
        verbose_name = "Trajet"
        verbose_name_plural = "Trajets"
        indexes = [
            models.Index(fields=["statut"]),
            models.Index(fields=["date_depart"]),
            models.Index(fields=["ville_depart"]),
            models.Index(fields=["ville_arrivee"]),
        ]
    
    def __str__(self):
        return f"{self.ville_depart} → {self.ville_arrivee} ({self.date_depart} {self.heure_depart})"
