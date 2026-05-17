from django.db import models
from django.utils import timezone
from users.models import Passager
from trajets.models import Trajet


class Reservation(models.Model):
    """Modèle pour les réservations"""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
        ('terminee', 'Terminée'),
    ]
    
    passager = models.ForeignKey(Passager, on_delete=models.CASCADE, related_name='reservations')
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name='reservations')
    
    # Détails de la réservation
    nombre_places = models.PositiveIntegerField(default=1)
    numero_siege = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Siège(s)',
        help_text='Numéros attribués automatiquement (ex. 3,4,5)',
    )
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    # Informations de récupération
    recupere = models.BooleanField(default=False, verbose_name="Passager récupéré")
    heure_recuperation = models.DateTimeField(null=True, blank=True)
    
    date_reservation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-date_reservation']
    
    def __str__(self):
        return f"Réservation {self.id} - {self.passager} - {self.trajet}"
    
    def confirmer(self):
        """Confirmer la réservation"""
        if self.statut == 'en_attente' and self.trajet.verifier_places(self.nombre_places):
            if not self.numero_siege:
                from .seats import attribuer_sieges_automatiquement
                self.numero_siege = attribuer_sieges_automatiquement(
                    self.trajet,
                    self.nombre_places,
                    self.passager,
                )
            self.prix_total = self.trajet.prix_base * self.nombre_places
            self.trajet.reserver_places(self.nombre_places)
            self.statut = 'confirmee'
            self.save()
            return True
        return False

    @property
    def sieges_attribues(self):
        from .seats import parse_sieges
        return parse_sieges(self.numero_siege)

    @property
    def sieges_affichage(self):
        sieges = self.sieges_attribues
        if not sieges:
            return ''
        if len(sieges) == 1:
            return f'Siège {sieges[0]}'
        return 'Sièges ' + ', '.join(sieges)
    
    def annuler(self):
        """Annuler la réservation"""
        if self.statut == 'confirmee':
            self.trajet.annuler_reservation(self.nombre_places)
            self.statut = 'annulee'
            self.save()
            return True
        if self.statut == 'en_attente':
            self.statut = 'annulee'
            self.save()
            return True
        return False

    def marquer_recupere(self):
        """Marquer un passager comme récupéré par le transporteur."""
        if self.statut != 'confirmee' or self.recupere:
            return False
        self.recupere = True
        self.heure_recuperation = timezone.now()
        self.save(update_fields=['recupere', 'heure_recuperation', 'date_modification'])
        return True


class Billet(models.Model):
    """Modèle pour les billets électroniques"""
    
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='billet')
    code_qr = models.CharField(max_length=255, unique=True)
    pdf = models.FileField(upload_to='billets/', blank=True)
    date_emission = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Billet"
        verbose_name_plural = "Billets"
    
    def __str__(self):
        return f"Billet {self.code_qr}"


class PointRamassage(models.Model):
    """Modèle pour les points de ramassage"""
    
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='points_ramassage')
    adresse = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    instructions = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Point de ramassage"
        verbose_name_plural = "Points de ramassage"
    
    def __str__(self):
        return f"Ramassage {self.reservation.id} - {self.adresse[:50]}"