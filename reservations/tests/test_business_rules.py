"""Tests des règles métier du modèle Reservation."""
from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from reservations.models import Reservation
from trajets.models import Trajet
from users.models import CustomUser, Passager, Transporteur


def _transporteur(licence_suffix: str) -> Transporteur:
    user = CustomUser.objects.create_user(
        username=f"tr_{licence_suffix}",
        email=f"tr_{licence_suffix}@test.com",
        password="TestPass123!",
        nom="Trans",
        prenom="Porteur",
        role="transporteur",
    )
    return Transporteur.objects.create(
        utilisateur=user,
        nom_entreprise="Co Test",
        numero_licence=f"LIC-{licence_suffix}",
    )


def _passager(suffix: str) -> Passager:
    user = CustomUser.objects.create_user(
        username=f"pa_{suffix}",
        email=f"pa_{suffix}@test.com",
        password="TestPass123!",
        nom="Pas",
        prenom="Sager",
        role="passager",
    )
    return Passager.objects.create(utilisateur=user)


class ReservationBusinessRulesTest(TestCase):
    def setUp(self):
        self.transporteur = _transporteur("res001")
        self.depart = timezone.now() + timedelta(hours=3)
        self.trajet = Trajet.objects.create(
            transporteur=self.transporteur,
            depart="A",
            destination="B",
            date_depart=self.depart,
            places_totales=10,
            places_disponibles=10,
            prix_base=Decimal("2000.00"),
        )

    def test_confirmer_calcule_prix_total(self):
        passager = _passager("001")
        reservation = Reservation.objects.create(
            passager=passager,
            trajet=self.trajet,
            nombre_places=2,
            prix_total=Decimal("0.00"),
            statut="en_attente",
        )
        self.assertTrue(reservation.confirmer())
        reservation.refresh_from_db()
        self.assertEqual(reservation.prix_total, Decimal("4000.00"))
        self.assertEqual(reservation.statut, "confirmee")

    def test_marquer_recupere_refuse_si_pas_confirmee(self):
        passager = _passager("002")
        reservation = Reservation.objects.create(
            passager=passager,
            trajet=self.trajet,
            nombre_places=1,
            prix_total=Decimal("2000.00"),
            statut="en_attente",
        )
        self.assertFalse(reservation.marquer_recupere())

    def test_marquer_recupere_ok_si_confirmee(self):
        passager = _passager("003")
        reservation = Reservation.objects.create(
            passager=passager,
            trajet=self.trajet,
            nombre_places=1,
            prix_total=Decimal("0.00"),
            statut="en_attente",
        )
        self.assertTrue(reservation.confirmer())
        self.assertTrue(reservation.marquer_recupere())
        reservation.refresh_from_db()
        self.assertTrue(reservation.recupere)
        self.assertIsNotNone(reservation.heure_recuperation)
