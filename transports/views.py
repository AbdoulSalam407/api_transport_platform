from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Transport
from .serializers import TransportSerializer


class TransportViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les transports.
    Fournit les actions CRUD standard:
    - LIST: GET /api/transports/
    - CREATE: POST /api/transports/
    - RETRIEVE: GET /api/transports/{id}/
    - UPDATE: PUT /api/transports/{id}/
    - DELETE: DELETE /api/transports/{id}/
    """
    
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    
    @action(detail=False, methods=["get"])
    def disponibles(self, request):
        """Endpoint personnalisé pour obtenir les transports disponibles"""
        transports = Transport.objects.filter(status="disponible")
        serializer = self.get_serializer(transports, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"])
    def changer_status(self, request, pk=None):
        """Endpoint pour changer le statut d'un transport"""
        transport = self.get_object()
        nouveau_status = request.data.get("status")
        
        if nouveau_status not in ["disponible", "en_cours", "maintenance"]:
            return Response(
                {"error": "Status invalide"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transport.status = nouveau_status
        transport.save()
        serializer = self.get_serializer(transport)
        return Response(serializer.data)
