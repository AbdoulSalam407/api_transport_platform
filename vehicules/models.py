from django.db import models
from users.models import Transporteur

class Marque(models.Model):
    """Marque du véhicule"""
    nom = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='marques/', blank=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Marque"
        verbose_name_plural = "Marques"


class Modele(models.Model):
    """Modèle du véhicule"""
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name='modeles')
    nom = models.CharField(max_length=100)
    nombre_places = models.PositiveIntegerField(default=4)
    
    def __str__(self):
        return f"{self.marque.nom} {self.nom}"
    
    class Meta:
        verbose_name = "Modèle"
        verbose_name_plural = "Modèles"
        unique_together = ['marque', 'nom']


class Vehicule(models.Model):
    """Véhicule d'un transporteur"""
    
    transporteur = models.ForeignKey(
        Transporteur,
        on_delete=models.CASCADE,
        related_name='vehicules'
    )
    modele = models.ForeignKey(Modele, on_delete=models.PROTECT)
    
    nombre_places = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Nombre de places passagers',
        help_text='Capacité réelle du véhicule (si différente du modèle).',
    )

    # Informations du véhicule
    immatriculation = models.CharField(max_length=20, unique=True, verbose_name="Immatriculation")
    couleur = models.CharField(max_length=50, blank=True)
    annee = models.PositiveIntegerField(verbose_name="Année de mise en circulation")
    
    # Statut
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    en_maintenance = models.BooleanField(default=False, verbose_name="En maintenance")
    
    # Caractéristiques
    climatisation = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    prise_usb = models.BooleanField(default=False)
    espace_bagages = models.CharField(max_length=100, blank=True)
    
    # Photos
    photo_principale = models.ImageField(upload_to='vehicules/', blank=True)
    
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.modele} - {self.immatriculation}"

    def clean(self):
        current_year = timezone.now().year + 1
        if self.annee < 1950 or self.annee > current_year:
            raise ValidationError("L'année du véhicule est invalide.")
        if self.en_maintenance and self.disponible:
            raise ValidationError("Un véhicule en maintenance ne peut pas être disponible.")
    
    @property
    def capacite_places(self):
        """Places passagers : valeur saisie par le transporteur ou capacité du modèle."""
        if self.nombre_places and self.nombre_places > 0:
            return self.nombre_places
        return self.modele.nombre_places

    @property
    def est_disponible(self):
        return self.disponible and not self.en_maintenance
    
    def marquer_maintenance(self):
        """Mettre le véhicule en maintenance"""
        self.en_maintenance = True
        self.disponible = False
        self.save()
    
    def marquer_disponible(self):
        """Rendre le véhicule disponible"""
        self.en_maintenance = False
        self.disponible = True
        self.save()
    
    class Meta:
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"