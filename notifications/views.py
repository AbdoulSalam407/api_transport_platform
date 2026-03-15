from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des notifications"""
    
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["type_notification", "is_read"]
    ordering_fields = ["date_creation"]
    
    def get_queryset(self):
        """Retourner les notifications de l'utilisateur connecté"""
        return Notification.objects.filter(utilisateur=self.request.user)
    
    @action(detail=True, methods=["post"])
    def marquer_comme_lue(self, request, pk=None):
        """Marquer une notification comme lue"""
        from django.utils import timezone
        
        notification = self.get_object()
        notification.is_read = True
        notification.date_lecture = timezone.now()
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=["post"])
    def marquer_tous_comme_lus(self, request):
        """Marquer toutes les notifications comme lues"""
        from django.utils import timezone
        
        notifications = self.get_queryset().filter(is_read=False)
        notifications.update(is_read=True, date_lecture=timezone.now())
        
        return Response({
            "message": f"{notifications.count()} notifications marquées comme lues"
        })
    
    @action(detail=False, methods=["get"])
    def non_lues(self, request):
        """Récupérer les notifications non lues"""
        notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
