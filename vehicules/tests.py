from django.test import TestCase
from .models import Vehicule


class VehiculeModelTest(TestCase):
    def setUp(self):
        self.vehicule = Vehicule.objects.create(
            marque="Toyota",
            modele="Hiace",
            plaque_immatriculation="ABC123",
            numero_chassis="VIN123",
            type_vehicule="minibus",
            capacite=14,
            annee_fabrication=2020,
            couleur="Blanc"
        )
    
    def test_vehicule_creation(self):
        self.assertEqual(self.vehicule.marque, "Toyota")
        self.assertEqual(self.vehicule.capacite, 14)
