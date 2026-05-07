from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    """Modèle de base pour tous les utilisateurs"""
    
    # Informations personnelles
    nom = models.CharField(max_length=150, verbose_name="Nom")
    prenom = models.CharField(max_length=150, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    
    # Rôle utilisateur
    ROLE_CHOICES = [
        ('passager', 'Passager'),
        ('transporteur', 'Transporteur'),
        ('admin', 'Administrateur'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='passager', verbose_name="Rôle")
    
    # Statut du compte
    is_verified = models.BooleanField(default=False, verbose_name="Vérifié")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    date_inscription = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    is_actif = models.BooleanField(default=True, verbose_name="Compte actif")
    
    # Photo de profil
    photo = models.ImageField(upload_to='profils/', blank=True, null=True)
    
    # Résolution des conflits avec AbstractUser
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nom', 'prenom', 'role']
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.role}"
    
    def seConnecter(self):
        """Méthode de connexion"""
        self.last_login = timezone.now()
        self.save()
        return True
    
    def seDeconnecter(self):
        """Méthode de déconnexion"""
        return True
    
    @property
    def est_passager(self):
        return hasattr(self, 'passager_profile')
    
    @property
    def est_transporteur(self):
        return hasattr(self, 'transporteur_profile')
    
    @property
    def est_admin(self):
        return self.role == 'admin' or self.is_superuser


class Passager(models.Model):
    """Modèle pour les passagers"""
    
    utilisateur = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='passager_profile'
    )
    
    # Préférences
    PREFERENCES_SIEGE = [
        ('fenetre', 'Fenêtre'),
        ('couloir', 'Couloir'),
        ('indifferent', 'Indifférent'),
    ]
    preferences_siege = models.CharField(
        max_length=20,
        choices=PREFERENCES_SIEGE,
        default='indifferent',
        verbose_name="Préférence de siège"
    )
    notifications_activees = models.BooleanField(default=True, verbose_name="Notifications actives")
    
    # Points de fidélité
    points_fidelite = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Passager"
        verbose_name_plural = "Passagers"
    
    def __str__(self):
        return f"Passager: {self.utilisateur.nom} {self.utilisateur.prenom}"
    
    def rechercherTrajet(self, depart, destination, date=None):
        """Rechercher un trajet selon des critères"""
        from trajets.models import Trajet
        
        queryset = Trajet.objects.filter(
            depart__icontains=depart,
            destination__icontains=destination,
            places_disponibles__gt=0,
            statut='actif'
        )
        
        if date:
            queryset = queryset.filter(date__date=date)
        
        return queryset
    
    def selectionnerSiege(self, reservation, numero_siege):
        """Sélectionner un siège pour un trajet"""
        reservation.numero_siege = numero_siege
        reservation.save()
        return True
    
    def definirPointRamassage(self, reservation_id, adresse, latitude, longitude):
        """Définir le point de ramassage pour une réservation"""
        from reservations.models import PointRamassage
        
        point = PointRamassage.objects.create(
            reservation_id=reservation_id,
            adresse=adresse,
            latitude=latitude,
            longitude=longitude
        )
        return point
    
    def recevoirBillet(self, reservation_id):
        """Recevoir le billet électronique"""
        from reservations.models import Billet
        
        try:
            billet = Billet.objects.get(reservation_id=reservation_id)
            return billet
        except Billet.DoesNotExist:
            return None
    
    def marquerRecupere(self, reservation_id):
        """Marquer que le passager a été récupéré"""
        from reservations.models import Reservation
        
        try:
            reservation = Reservation.objects.get(id=reservation_id, passager=self)
            reservation.recupere = True
            reservation.save()
            return True
        except Reservation.DoesNotExist:
            return False


class Transporteur(models.Model):
    """Modèle pour les transporteurs"""
    
    utilisateur = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='transporteur_profile'
    )
    
    # Informations professionnelles
    nom_entreprise = models.CharField(max_length=200, verbose_name="Nom de l'entreprise")
    numero_licence = models.CharField(max_length=50, unique=True, verbose_name="Numéro de licence")
    verifie = models.BooleanField(default=False, verbose_name="Compte vérifié")
    note_moyenne = models.FloatField(default=0.0, verbose_name="Note moyenne")
    
    # Documents
    licence_pdf = models.FileField(upload_to='licences/', blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True)
    
    # Configuration
    est_ouvert = models.BooleanField(default=True, verbose_name="Accepte les réservations")
    
    class Meta:
        verbose_name = "Transporteur"
        verbose_name_plural = "Transporteurs"
    
    def __str__(self):
        return f"{self.nom_entreprise} ({self.utilisateur.nom})"
    
    def creerTrajet(self, trajet_data):
        """Créer un nouveau trajet"""
        from trajets.models import Trajet
        
        trajet_data['transporteur'] = self
        trajet = Trajet.objects.create(**trajet_data)
        return trajet
    
    def modifierTrajet(self, trajet_id, **kwargs):
        """Modifier un trajet existant"""
        from trajets.models import Trajet
        
        try:
            trajet = Trajet.objects.get(id=trajet_id, transporteur=self)
            for key, value in kwargs.items():
                setattr(trajet, key, value)
            trajet.save()
            return True
        except Trajet.DoesNotExist:
            return False
    
    def supprimerTrajet(self, trajet_id):
        """Supprimer un trajet"""
        from trajets.models import Trajet
        
        try:
            trajet = Trajet.objects.get(id=trajet_id, transporteur=self)
            trajet.delete()
            return True
        except Trajet.DoesNotExist:
            return False
    
    def notifierPassagersDepart(self, trajet_id):
        """Notifier les passagers du départ imminent"""
        from reservations.models import Reservation
        from notifications.models import Notification
        
        reservations = Reservation.objects.filter(
            trajet_id=trajet_id,
            statut='confirmee'
        )
        
        notifications_created = []
        for reservation in reservations:
            notif = Notification.objects.create(
                utilisateur=reservation.passager.utilisateur,
                type='depart_imminent',
                titre="Départ imminent",
                message=f"Votre trajet #{trajet_id} va bientôt démarrer!",
                reservation=reservation
            )
            notifications_created.append(notif)
        
        return notifications_created


class Administrateur(models.Model):
    """Modèle pour les administrateurs"""
    
    utilisateur = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='admin_profile'
    )
    
    NIVEAUX_ACCES = [
        ('complet', 'Accès complet'),
        ('moderation', 'Modération seule'),
        ('lecture', 'Lecture seule'),
    ]
    niveau_acces = models.CharField(
        max_length=20,
        choices=NIVEAUX_ACCES,
        default='complet',
        verbose_name="Niveau d'accès"
    )
    
    class Meta:
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"
    
    def __str__(self):
        return f"Admin: {self.utilisateur.nom} {self.utilisateur.prenom}"
    
    def gererUtilisateur(self, utilisateur_id, action, **kwargs):
        """Gérer un utilisateur (activer/désactiver/modifier)"""
        try:
            user = CustomUser.objects.get(id=utilisateur_id)
            
            if action == 'desactiver':
                user.is_actif = False
            elif action == 'activer':
                user.is_actif = True
            elif action == 'modifier':
                for key, value in kwargs.items():
                    setattr(user, key, value)
            
            user.save()
            return True
        except CustomUser.DoesNotExist:
            return False
    
    def validerTransporteur(self, transporteur_id):
        """Valider un compte transporteur"""
        try:
            transporteur = Transporteur.objects.get(utilisateur_id=transporteur_id)
            transporteur.verifie = True
            transporteur.save()
            return True
        except Transporteur.DoesNotExist:
            return False
    
    def consulterStatistique(self, type_stat, periode=None):
        """Consulter les statistiques"""
        # from statistiques.models import Statistique  # Quand l'app sera créée
        return None
    
    def ajouterUtilisateur(self, user_data):
        """Ajouter un nouvel utilisateur"""
        user = CustomUser.objects.create_user(**user_data)
        return user
    
    def supprimerUtilisateur(self, utilisateur_id):
        """Supprimer un utilisateur"""
        try:
            CustomUser.objects.get(id=utilisateur_id).delete()
            return True
        except CustomUser.DoesNotExist:
            return False
    
    def verifierUtilisateur(self, utilisateur_id):
        """Vérifier les informations d'un utilisateur"""
        try:
            user = CustomUser.objects.get(id=utilisateur_id)
            return {
                'existe': True,
                'actif': user.is_actif,
                'role': user.role,
                'email_verifie': user.is_verified
            }
        except CustomUser.DoesNotExist:
            return {'existe': False}