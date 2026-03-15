from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Vehicule(models.Model):
    """Modèle pour les véhicules"""
    
    TYPE_CHOICES = [
        ("bus", "Bus"),
        ("minibus", "Minibus"),
        ("voiture", "Voiture"),
        ("van", "Van"),
    ]
    
    STATUS_CHOICES = [
        ("disponible", "Disponible"),
        ("en_trajet", "En trajet"),
        ("maintenance", "Maintenance"),
        ("inactif", "Inactif"),
    ]
    
    chauffeur = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "driver"},
        related_name="vehicule",
        verbose_name="Chauffeur"
    )
    
    marque = models.CharField(max_length=50, verbose_name="Marque")
    modele = models.CharField(max_length=50, verbose_name="Modèle")
    plaque_immatriculation = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Plaque d'immatriculation"
    )
    numero_chassis = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Numéro de chassis"
    )
    type_vehicule = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type"
    )
    capacite = models.PositiveIntegerField(verbose_name="Capacité (places)")
    annee_fabrication = models.IntegerField(verbose_name="Année de fabrication")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="disponible",
        verbose_name="Statut"
    )
    couleur = models.CharField(max_length=30, verbose_name="Couleur")
    photo = models.ImageField(
        upload_to="vehicules/",
        null=True,
        blank=True,
        verbose_name="Photo"
    )
    assurance_date_expiration = models.DateField(verbose_name="Date expiration assurance")
    controle_technique_date = models.DateField(verbose_name="Date contrôle technique")
    kilometrage = models.IntegerField(default=0, verbose_name="Kilométrage")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"
    
    def __str__(self):
        return f"{self.marque} {self.modele} - {self.plaque_immatriculation}"
