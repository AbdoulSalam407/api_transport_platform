from django.db import models


class Transport(models.Model):
    """Modèle pour la gestion des transports"""
    
    STATUS_CHOICES = [
        ("disponible", "Disponible"),
        ("en_cours", "En cours"),
        ("maintenance", "Maintenance"),
    ]
    
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # Bus, Taxi, Van, etc.
    plaque_immatriculation = models.CharField(max_length=20, unique=True)
    capacite = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="disponible"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Transport"
        verbose_name_plural = "Transports"
    
    def __str__(self):
        return f"{self.nom} - {self.plaque_immatriculation}"
