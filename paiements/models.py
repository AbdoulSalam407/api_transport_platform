from django.db import models
from users.models import CustomUser
from reservations.models import Reservation


class Paiement(models.Model):
    """Modèle pour les paiements"""
    
    METHODE_CHOICES = [
        ('carte', 'Carte bancaire'),
        ('mobile_money', 'Mobile Money'),
        ('paypal', 'PayPal'),
        ('especes', 'Espèces'),
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('reussi', 'Réussi'),
        ('echoue', 'Échoué'),
        ('rembourse', 'Remboursé'),
    ]
    
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='paiements')
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='paiement')
    
    # Détails du paiement
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    methode = models.CharField(max_length=20, choices=METHODE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    # Transaction externe
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    reference_externe = models.CharField(max_length=100, blank=True)
    
    # Informations de paiement
    data_paiement = models.JSONField(default=dict, blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Paiement {self.id} - {self.montant}€ - {self.statut}"
    
    def valider(self):
        """Valider le paiement"""
        from django.utils import timezone
        self.statut = 'reussi'
        self.date_validation = timezone.now()
        self.save()
        
        # Confirmer la réservation
        self.reservation.confirmer()
        return True
    
    def echouer(self):
        """Marquer le paiement comme échoué"""
        self.statut = 'echoue'
        self.save()
        return True
    
    def rembourser(self):
        """Rembourser le paiement"""
        self.statut = 'rembourse'
        self.save()
        return True


class TransactionLog(models.Model):
    """Log des transactions pour traçabilité"""
    
    paiement = models.ForeignKey(Paiement, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=100)
    statut = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    data = models.JSONField(default=dict, blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Log de transaction"
        verbose_name_plural = "Logs de transactions"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.action} - {self.statut} - {self.date_creation}"