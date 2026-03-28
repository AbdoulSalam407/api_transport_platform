from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Marque, Modele, Vehicule
from .serializers import MarqueSerializer, ModeleSerializer, VehiculeSerializer
from core.permissions import IsAdmin, IsTransporteur, IsAdminOrTransporteur


class MarqueViewSet(viewsets.ModelViewSet):
    """CRUD pour les marques"""
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializer
    permission_classes = [IsAdminOrTransporteur]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()


class ModeleViewSet(viewsets.ModelViewSet):
    """CRUD pour les modèles"""
    queryset = Modele.objects.all()
    serializer_class = ModeleSerializer
    permission_classes = [IsAdminOrTransporteur]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset = Modele.objects.all()
        marque_id = self.request.query_params.get('marque', None)
        if marque_id:
            queryset = queryset.filter(marque_id=marque_id)
        return queryset


class VehiculeViewSet(viewsets.ModelViewSet):
    """CRUD pour les véhicules"""
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer
    permission_classes = [IsAdminOrTransporteur]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Vehicule.objects.all()
        elif user.est_transporteur:
            return Vehicule.objects.filter(transporteur__utilisateur=user)
        return Vehicule.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.est_transporteur:
            transporteur = self.request.user.transporteur_profile
            serializer.save(transporteur=transporteur)
        else:
            serializer.save()


class MettreVehiculeDisponibleView(APIView):
    """Mettre un véhicule disponible"""
    permission_classes = [IsAdminOrTransporteur]
    
    def post(self, request, pk):
        try:
            vehicule = Vehicule.objects.get(id=pk)
            
            # Vérifier que le transporteur possède le véhicule
            if request.user.est_transporteur:
                if vehicule.transporteur.utilisateur != request.user:
                    return Response(
                        {'error': 'Vous ne possédez pas ce véhicule'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            vehicule.marquer_disponible()
            return Response({'message': 'Véhicule disponible'})
        except Vehicule.DoesNotExist:
            return Response(
                {'error': 'Véhicule non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )


class MettreVehiculeMaintenanceView(APIView):
    """Mettre un véhicule en maintenance"""
    permission_classes = [IsAdminOrTransporteur]
    
    def post(self, request, pk):
        try:
            vehicule = Vehicule.objects.get(id=pk)
            
            # Vérifier que le transporteur possède le véhicule
            if request.user.est_transporteur:
                if vehicule.transporteur.utilisateur != request.user:
                    return Response(
                        {'error': 'Vous ne possédez pas ce véhicule'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            vehicule.marquer_maintenance()
            return Response({'message': 'Véhicule en maintenance'})
        except Vehicule.DoesNotExist:
            return Response(
                {'error': 'Véhicule non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )


class VehiculesParTransporteurView(generics.ListAPIView):
    """Lister les véhicules d'un transporteur"""
    serializer_class = VehiculeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        transporteur_id = self.kwargs['transporteur_id']
        return Vehicule.objects.filter(transporteur_id=transporteur_id)