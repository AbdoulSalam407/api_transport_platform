from rest_framework import viewsets
from .models import Passager, Transporteur
from .serializers import PassagerSerializer, TransporteurSerializer

class PassagerViewSet(viewsets.ModelViewSet):
    queryset = Passager.objects.all()
    serializer_class = PassagerSerializer

class TransporteurViewSet(viewsets.ModelViewSet):
    queryset = Transporteur.objects.all()
    serializer_class = TransporteurSerializer