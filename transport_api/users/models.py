from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    PASSAGER = "PASSAGER", "Passager"
    TRANSPORTEUR = "TRANSPORTEUR", "Transporteur"


class User(AbstractUser):
    """Utilisateur de base : nom, prénom, email, mot de passe (hérité), rôle."""

    email = models.EmailField("email", unique=True)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PASSAGER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "nom", "prenom"]

    def __str__(self):
        return f"{self.prenom} {self.nom} <{self.email}>"


class Passager(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="passager_profile",
        primary_key=True,
    )
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return f"Passager {self.user.email}"


class ValidationStatut(models.TextChoices):
    EN_ATTENTE = "en_attente", "En attente"
    VALIDE = "valide", "Validé"
    REFUSE = "refuse", "Refusé"


class Transporteur(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="transporteur_profile",
        primary_key=True,
    )
    nom_compagnie = models.CharField(max_length=200)
    licence = models.CharField(max_length=100)
    statut_validation = models.CharField(
        max_length=20,
        choices=ValidationStatut.choices,
        default=ValidationStatut.EN_ATTENTE,
    )

    def __str__(self):
        return f"{self.nom_compagnie} ({self.user.email})"
