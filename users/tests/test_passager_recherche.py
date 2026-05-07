"""Tests de la recherche de trajets côté Passager."""
from datetime import datetime, time
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from trajets.models import Trajet
from users.models import CustomUser, Passager, Transporteur


def _transporteur(licence: str) -> Transporteur:
    user = CustomUser.objects.create_user(
        username=f"u_{licence}",
        email=f"u_{licence}@test.com",
        password="TestPass123!",
        nom="T",
        prenom="T",
        role="transporteur",
    )
    return Transporteur.objects.create(
        utilisateur=user,
        nom_entreprise="Co",
        numero_licence=licence,
    )


class PassagerRechercherTrajetTest(TestCase):
    def setUp(self):
        self.transporteur = _transporteur("LIC-RECH-1")
        self.passager_user = CustomUser.objects.create_user(
            username="pass_rech",
            email="pass_rech@test.com",
            password="TestPass123!",
            nom="P",
            prenom="A",
            role="passager",
        )
        self.passager = Passager.objects.create(utilisateur=self.passager_user)
        self.today = timezone.localdate()
        self.depart_dt = timezone.make_aware(
            datetime.combine(self.today, time(8, 0))
        )

    def test_filtre_par_date_utilise_date_depart(self):
        Trajet.objects.create(
            transporteur=self.transporteur,
            depart="Dakar",
            destination="Saint-Louis",
            date_depart=self.depart_dt,
            places_totales=20,
            places_disponibles=15,
            prix_base=Decimal("5000.00"),
        )
        qs = self.passager.rechercherTrajet(
            "Dakar", "Saint-Louis", date=self.today
        )
        self.assertEqual(qs.count(), 1)
