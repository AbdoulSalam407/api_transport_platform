from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    """Modèle de base pour tous les utilisateurs"""
    
    # Attributs du diagramme
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[
        ('passager', 'Passager'),
        ('transporteur', 'Transporteur'),
        ('admin', 'Administrateur'),
    ])
    is_verified = models.BooleanField(default=False)    
    
    # Informations supplémentaires
    telephone = models.CharField(max_length=15, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    is_actif = models.BooleanField(default=True)
    
    # Résolution des conflits avec auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.role}"
    
    def seConnecter(self):
        """Méthode de connexion"""
        self.last_login = timezone.now()
        self.save()
        return True
    
    def seDeconnecter(self):
        """Méthode de déconnexion"""
        # Logique de déconnexion
        return True
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


class Passager(models.Model):
    """Modèle pour les passagers"""
    
    utilisateur = models.OneToOneField(
        CustomUser , 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='passager_profile'
    )
    
    # Préférences
    preferences_siege = models.CharField(max_length=50, default='indifferent')
    notifications_activees = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Passager: {self.utilisateur.nom}"
    
    def rechercherTrajet(self, depart, destination, date):
        """Rechercher un trajet selon des critères"""
        from trajets.models import Trajet
        return Trajet.objects.filter(
            depart=depart,
            destination=destination,
            date=date,
            places_disponibles__gt=0
        )
    
    def selectionnerSiege(self, trajet_id, numero_siege):
        """Sélectionner un siège pour un trajet"""
        # Logique de sélection de siège
        return True
    
    def definirPointRamassage(self, reservation_id, adresse, coordonnees):
        """Définir le point de ramassage pour une réservation"""
        from reservations.models import PointRamassage
        point = PointRamassage.objects.create(
            reservation_id=reservation_id,
            adresse=adresse,
            coordonnees_gps=coordonnees
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
    
    def marquerRecuperer(self, reservation_id):
        """Marquer que le passager a été récupéré"""
        from reservations.models import Reservation
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.recupere = True
            reservation.save()
            return True
        except Reservation.DoesNotExist:
            return False


class Administrateur(models.Model):
    """Modèle pour les administrateurs"""
    
    utilisateur = models.OneToOneField(
        CustomUser , 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='admin_profile'
    )
    
    niveau_acces = models.CharField(max_length=50, default='complet')
    
    def __str__(self):
        return f"Admin: {self.utilisateur.nom}"
    
    def gererUtilisateur(self, utilisateur_id, action, **kwargs):
        """Gérer un utilisateur (activer/désactiver/modifier)"""
        try:
            user = CustomUser.objects.get(id=utilisateur_id)
            if action == 'desactiver':
                user.est_actif = False
            elif action == 'activer':
                user.est_actif = True
            elif action == 'modifier':
                for key, value in kwargs.items():
                    setattr(user, key, value)
            user.save()
            return True
        except CustomUser.DoesNotExist:
            return False
    
    def validerTransporteur(self, transporteur_id):
        """Valider un compte transporteur"""
        from users.models import Transporteur
        try:
            transporteur = Transporteur.objects.get(utilisateur_id=transporteur_id)
            transporteur.verifie = True
            transporteur.save()
            return True
        except Transporteur.DoesNotExist:
            return False
    
    def consulterStatistique(self, type_stat, periode):
        """Consulter les statistiques"""
        from statistiques.models import Statistique
        return Statistique.objects.filter(
            type=type_stat,
            periode=periode
        ).first()
    
    def gererNotification(self, notification_id, action):
        """Gérer les notifications"""
        from notifications.models import Notification
        try:
            notif = Notification.objects.get(id=notification_id)
            if action == 'supprimer':
                notif.delete()
            elif action == 'marquer_lue':
                notif.est_lu = True
                notif.save()
            return True
        except Notification.DoesNotExist:
            return False
    
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
                'actif': user.est_actif,
                'role': user.role,
                'email_verifie': user.email.endswith('.com')  # Simplifié
            }
        except CustomUser.DoesNotExist:
            return {'existe': False}


class Transporteur(models.Model):
    """Modèle pour les transporteurs"""
    
    utilisateur = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='transporteur_profile'
    )
    
    # Informations spécifiques
    nom_entreprise = models.CharField(max_length=200, blank=True)
    numero_licence = models.CharField(max_length=50, unique=True)
    verifie = models.BooleanField(default=False)
    note_moyenne = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"Transporteur: {self.utilisateur.nom} ({self.nom_entreprise})"
    
    def gererTrajet(self, trajet_id, action, **kwargs):
        """Gérer un trajet (modifier/supprimer)"""
        from trajets.models import Trajet
        try:
            trajet = Trajet.objects.get(id=trajet_id, transporteur=self)
            if action == 'modifier':
                for key, value in kwargs.items():
                    setattr(trajet, key, value)
                trajet.save()
            elif action == 'supprimer':
                trajet.delete()
            return True
        except Trajet.DoesNotExist:
            return False
    
    def modifierTrajet(self, trajet_id, **kwargs):
        """Modifier un trajet existant"""
        return self.gererTrajet(trajet_id, 'modifier', **kwargs)
    
    def supprimerTrajet(self, trajet_id):
        """Supprimer un trajet"""
        return self.gererTrajet(trajet_id, 'supprimer')
    
    def creerTrajet(self, trajet_data):
        """Créer un nouveau trajet"""
        from trajets.models import Trajet
        trajet_data['transporteur'] = self
        trajet = Trajet.objects.create(**trajet_data)
        return trajet
    
    def notifierPassagersDepart(self, trajet_id):
        """Notifier les passagers du départ imminent"""
        from reservations.models import Reservation
        from notifications.models import Notification
        
        reservations = Reservation.objects.filter(
            trajet_id=trajet_id,
            statut='confirmee'
        )
        
        for reservation in reservations:
            Notification.objects.create(
                utilisateur=reservation.passager.utilisateur,
                type='depart',
                message=f"Votre trajet va bientôt démarrer!",
                reservation=reservation
            )
        return True
    
    def ajouterVehicule(self, vehicule_data):
        """Ajouter un nouveau véhicule"""
        from vehicules.models import Vehicule
        vehicule_data['transporteur'] = self
        vehicule = Vehicule.objects.create(**vehicule_data)
        return vehicule
    
    
    def listerVehicules(self):
        """Lister tous les véhicules du transporteur"""
        return self.vehicules.all()
    
    def getVehiculeActif(self):
        """Obtenir le véhicule actuellement utilisé"""
        return self.vehicules.filter(disponible=True, en_maintenance=False).first() 
