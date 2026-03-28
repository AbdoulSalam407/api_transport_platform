from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer, NotificationMarquerLueSerializer
from core.permissions import IsAdmin


class NotificationViewSet(viewsets.ModelViewSet):
    """CRUD pour les notifications"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'admin':
            return Notification.objects.all()
        else:
            return Notification.objects.filter(utilisateur=user)


class MesNotificationsView(generics.ListAPIView):
    """Lister mes notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(
            utilisateur=self.request.user
        ).order_by('-date_creation')


class NotificationsNonLuesView(generics.ListAPIView):
    """Lister les notifications non lues"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(
            utilisateur=self.request.user,
            est_lu=False
        ).order_by('-date_creation')


class CompterNotificationsNonLuesView(APIView):
    """Compter les notifications non lues"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        count = Notification.objects.filter(
            utilisateur=request.user,
            est_lu=False
        ).count()
        
        return Response({'non_lues': count})


class MarquerNotificationLueView(APIView):
    """Marquer une notification comme lue"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            notification = Notification.objects.get(
                id=pk,
                utilisateur=request.user
            )
            
            notification.marquer_lue()
            
            return Response({
                'message': 'Notification marquée comme lue',
                'notification': NotificationSerializer(notification).data
            })
            
        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notification non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )


class MarquerNotificationsLuesView(APIView):
    """Marquer plusieurs notifications comme lues"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = NotificationMarquerLueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if serializer.validated_data.get('tout_marquer'):
            # Marquer toutes les notifications comme lues
            notifications = Notification.objects.filter(
                utilisateur=request.user,
                est_lu=False
            )
        else:
            # Marquer seulement les notifications spécifiées
            notification_ids = serializer.validated_data.get('notification_ids', [])
            notifications = Notification.objects.filter(
                id__in=notification_ids,
                utilisateur=request.user,
                est_lu=False
            )
        
        count = notifications.count()
        
        for notification in notifications:
            notification.marquer_lue()
        
        return Response({
            'message': f'{count} notification(s) marquée(s) comme lue(s)',
            'marquees': count
        })


class SupprimerNotificationView(APIView):
    """Supprimer une notification"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, pk):
        try:
            notification = Notification.objects.get(
                id=pk,
                utilisateur=request.user
            )
            
            notification.delete()
            
            return Response(
                {'message': 'Notification supprimée'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notification non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )


class SupprimerToutesNotificationsView(APIView):
    """Supprimer toutes mes notifications"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request):
        count = Notification.objects.filter(
            utilisateur=request.user
        ).delete()[0]
        
        return Response(
            {'message': f'{count} notification(s) supprimée(s)'},
            status=status.HTTP_204_NO_CONTENT
        )


class CreerNotificationView(APIView):
    """Créer une notification (admin uniquement)"""
    permission_classes = [IsAdmin]
    
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NotifierPassagersView(APIView):
    """Notifier les passagers d'un trajet (transporteur)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, trajet_id):
        try:
            from trajets.models import Trajet
            
            trajet = Trajet.objects.get(
                id=trajet_id,
                transporteur__utilisateur=request.user
            )
            
            notifications_created = trajet.notifierPassagersDepart()
            
            return Response({
                'message': f'{len(notifications_created)} notification(s) envoyée(s)',
                'notifications': NotificationSerializer(notifications_created, many=True).data
            })
            
        except Trajet.DoesNotExist:
            return Response(
                {'error': 'Trajet non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )