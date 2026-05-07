"""Tests des règles métier du modèle Trajet."""
from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from trajets.models import Trajet
from users.models import CustomUser, Transporteur


def _transporteur(licence_suffix: str) -> Transporteur:
    user = CustomUser.objects.create_user(
        username=f"trans_{licence_suffix}",
        email=f"trans_{licence_suffix}@test.com",
        password="TestPass123!",
        nom="Trans",
        prenom="Porteur",
        role="transporteur",
    )
    return Transporteur.objects.create(
        utilisateur=user,
        nom_entreprise="Entreprise Test",
        numero_licence=f"LIC-{licence_suffix}",
    )


class TrajetBusinessRulesTest(TestCase):
    def setUp(self):
        self.transporteur = _transporteur("001")
        self.base = timezone.now() + timedelta(hours=2)

    def test_places_totales_zero_raises_validation_error(self):
        trajet = Trajet(
            transporteur=self.transporteur,
            depart="Dakar",
            destination="Thiès",
            date_depart=self.base,
            places_totales=0,
            places_disponibles=0,
            prix_base=Decimal("1000.00"),
        )
        with self.assertRaises(ValidationError):
            trajet.full_clean()

    def test_places_disponibles_superieures_places_totales_raises(self):
        trajet = Trajet(
            transporteur=self.transporteur,
            depart="Dakar",
            destination="Thiès",
            date_depart=self.base,
            places_totales=5,
            places_disponibles=10,
            prix_base=Decimal("1000.00"),
        )
        with self.assertRaises(ValidationError):
            trajet.full_clean()

    def test_save_marks_complet_when_no_places_left(self):
        trajet = Trajet.objects.create(
            transporteur=self.transporteur,
            depart="Dakar",
            destination="Thiès",
            date_depart=self.base,
            places_totales=3,
            places_disponibles=0,
            prix_base=Decimal("1500.00"),
        )
        trajet.refresh_from_db()
        self.assertEqual(trajet.statut, "complet")

    def test_annuler_reservation_ne_depasse_pas_capacite(self):
        trajet = Trajet.objects.create(
            transporteur=self.transporteur,
            depart="Dakar",
            destination="Thiès",
            date_depart=self.base,
            places_totales=5,
            places_disponibles=0,
            prix_base=Decimal("1500.00"),
        )
        trajet.annuler_reservation(10)
        trajet.refresh_from_db()
        self.assertEqual(trajet.places_disponibles, 5)
