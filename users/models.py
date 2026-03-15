from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """Modèle utilisateur personnalisé"""
    
    ROLE_CHOICES = [
        ("client", "Client"),
        ("driver", "Conducteur"),
        ("admin", "Administrateur"),
    ]
    
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Le numéro de téléphone doit être au format international"
    )
    
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True,
        verbose_name="Numéro de téléphone"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="client",
        verbose_name="Rôle"
    )
    profile_picture = models.ImageField(
        upload_to="profiles/",
        null=True,
        blank=True,
        verbose_name="Photo de profil"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Biographie"
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Vérifié"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'inscription"
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Dernière connexion"
    )
    
    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
