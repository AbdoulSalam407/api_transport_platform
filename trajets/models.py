from django.db import models
from users.models import Transporteur


class Trajet(models.Model):
    """Modèle pour les trajets"""
    
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('complet', 'Complet'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]
    
    # Relations
    transporteur = models.ForeignKey(
        Transporteur,
        on_delete=models.CASCADE,
        related_name='trajets'
    )
    
    vehicule = models.ForeignKey(
        'vehicules.Vehicule',
        on_delete=models.CASCADE,
        related_name="trajets",
        verbose_name="Véhicule",
        null=True,
        blank=True
    )
    
    chauffeur = models.ForeignKey(
        Transporteur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trajets_conduits",
        verbose_name="Chauffeur"
    )
    
    # Informations du trajet
    depart = models.CharField(max_length=200, verbose_name="Lieu de départ")
    destination = models.CharField(max_length=200, verbose_name="Destination")
    date_depart = models.DateTimeField(verbose_name="Date et heure de départ")
    date_arrivee_estimee = models.DateTimeField(
        verbose_name="Date et heure d'arrivée estimée",
        null=True,
        blank=True
    )
    date_arrivee_reelle = models.DateTimeField(
        verbose_name="Date et heure d'arrivée réelle",
        null=True,
        blank=True
    )
    
    # Capacité et prix
    places_totales = models.PositiveIntegerField(verbose_name="Nombre total de places")
    places_disponibles = models.PositiveIntegerField(verbose_name="Places disponibles")
    prix_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix par place"
    )
    
    # Distance et durée
    distance_km = models.FloatField(verbose_name="Distance (km)", null=True, blank=True)
    duree_estimee = models.DurationField(verbose_name="Durée estimée", null=True, blank=True)
    
    # Statut
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    
    # Informations supplémentaires
    description = models.TextField(blank=True)
    
    # GPS et tracé
    latitude_depart = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude_depart = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    latitude_arrivee = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude_arrivee = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    
    # Points d'arrêt (JSON)
    points_arret = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Points d'arrêt"
    )
    
    # Horaires des arrêts (JSON) - conservé pour compatibilité
    arrets = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Liste des arrêts"
    )
    
    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Trajet"
        verbose_name_plural = "Trajets"
        ordering = ['-date_depart']
        indexes = [
            models.Index(fields=['statut']),
            models.Index(fields=['date_depart']),
        ]
    
    def __str__(self):
        return f"{self.depart} → {self.destination} ({self.date_depart.strftime('%d/%m/%Y %H:%M')})"
    
    def verifier_places(self, nombre=1):
        """Vérifier si des places sont disponibles"""
        return self.places_disponibles >= nombre
    
    def reserver_places(self, nombre=1):
        """Réserver des places"""
        if self.verifier_places(nombre):
            self.places_disponibles -= nombre
            if self.places_disponibles == 0:
                self.statut = 'complet'
            self.save()
            return True
        return False
    
    def annuler_reservation(self, nombre=1):
        """Annuler une réservation"""
        self.places_disponibles += nombre
        if self.statut == 'complet' and self.places_disponibles > 0:
            self.statut = 'actif'
        self.save()
        return True
    
    @property
    def places_reservees(self):
        return self.places_totales - self.places_disponibles
    
    @property
    def taux_remplissage(self):
        if self.places_totales == 0:
            return 0
        return (self.places_reservees / self.places_totales) * 100


class Etape(models.Model):
    """Étapes intermédiaires du trajet"""
    
    trajet = models.ForeignKey(
        Trajet,
        on_delete=models.CASCADE,
        related_name='etapes'
    )
    lieu = models.CharField(max_length=200)
    heure_prevue = models.DateTimeField()
    heure_reelle = models.DateTimeField(null=True, blank=True)
    ordre = models.PositiveIntegerField()
    
    class Meta:
        verbose_name = "Étape"
        verbose_name_plural = "Étapes"
        ordering = ['trajet', 'ordre']
    
    def __str__(self):
        return f"{self.trajet} - {self.lieu} ({self.ordre})"