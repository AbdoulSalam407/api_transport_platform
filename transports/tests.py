from django.test import TestCase
from rest_framework.test import APIClient
from .models import Transport


class TransportAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.transport = Transport.objects.create(
            nom="Bus 101",
            type="Bus",
            plaque_immatriculation="ABC123",
            capacite=50,
            status="disponible"
        )
    
    def test_get_transports(self):
        """Test pour récupérer la liste des transports"""
        response = self.client.get("/api/transports/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    
    def test_create_transport(self):
        """Test pour créer un nouveau transport"""
        data = {
            "nom": "Taxi 002",
            "type": "Taxi",
            "plaque_immatriculation": "XYZ789",
            "capacite": 4,
            "status": "disponible"
        }
        response = self.client.post("/api/transports/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transport.objects.count(), 2)
