from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserDetailSerializer, UserCreateSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des utilisateurs"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "retrieve":
            return UserDetailSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Récupérer l'utilisateur connecté"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Changer le mot de passe de l'utilisateur"""
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        
        if not request.user.check_password(old_password):
            return Response(
                {"error": "Ancien mot de passe incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.set_password(new_password)
        request.user.save()
        return Response({"message": "Mot de passe changé avec succès"})
