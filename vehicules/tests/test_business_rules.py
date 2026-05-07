"""Tests des validations métier du modèle Vehicule."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from users.models import CustomUser, Transporteur
from vehicules.models import Marque, Modele, Vehicule


def _transporteur(licence_suffix: str) -> Transporteur:
    user = CustomUser.objects.create_user(
        username=f"tv_{licence_suffix}",
        email=f"tv_{licence_suffix}@test.com",
        password="TestPass123!",
        nom="Trans",
        prenom="Porteur",
        role="transporteur",
    )
    return Transporteur.objects.create(
        utilisateur=user,
        nom_entreprise="Co",
        numero_licence=f"LIC-V-{licence_suffix}",
    )


class VehiculeBusinessRulesTest(TestCase):
    def setUp(self):
        self.transporteur = _transporteur("v001")
        self.marque = Marque.objects.create(nom="MarqueTest")
        self.modele = Modele.objects.create(
            marque=self.marque, nom="Bus500", nombre_places=50
        )

    def test_annee_invalide_raises(self):
        vehicule = Vehicule(
            transporteur=self.transporteur,
            modele=self.modele,
            immatriculation="XX-001-AA",
            annee=1800,
        )
        with self.assertRaises(ValidationError):
            vehicule.full_clean()

    def test_maintenance_et_disponible_incompatible(self):
        vehicule = Vehicule(
            transporteur=self.transporteur,
            modele=self.modele,
            immatriculation="XX-002-AA",
            annee=timezone.now().year - 2,
            en_maintenance=True,
            disponible=True,
        )
        with self.assertRaises(ValidationError):
            vehicule.full_clean()
