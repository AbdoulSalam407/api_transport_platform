from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db import transaction
from .models import CustomUser, Passager, Transporteur, Administrateur
from .serializers import (
    UserSerializer, UserCreateSerializer, UserProfileSerializer,
    PassagerSerializer, TransporteurSerializer, AdministrateurSerializer,
    LoginSerializer, ChangePasswordSerializer
)
from core.permissions import IsAdmin, IsAdminOrSelf, IsAuthenticatedOrReadOnly

# ==================== AUTHENTIFICATION ====================

class RegisterView(generics.CreateAPIView):
    """Inscription d'un nouvel utilisateur"""
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            # Créer l'utilisateur
            user = CustomUser.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                nom=serializer.validated_data['nom'],
                prenom=serializer.validated_data['prenom'],
                telephone=serializer.validated_data.get('telephone', ''),
                role=serializer.validated_data['role']
            )
            
            # Créer le profil selon le rôle
            if user.role == 'passager':
                Passager.objects.create(utilisateur=user)
            elif user.role == 'transporteur':
                Transporteur.objects.create(
                    utilisateur=user,
                    nom_entreprise=serializer.validated_data.get('nom_entreprise', ''),
                    numero_licence=serializer.validated_data.get('numero_licence', '')
                )
            elif user.role == 'admin':
                Administrateur.objects.create(utilisateur=user)
        
        # Créer un token pour l'utilisateur
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Connexion d'un utilisateur"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Vérifier si l'utilisateur existe avec cet email
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'Email ou mot de passe incorrect'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Authentifier l'utilisateur
        user = authenticate(username=user.username, password=password)
        
        if not user:
            return Response(
                {'error': 'Email ou mot de passe incorrect'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_actif:
            return Response(
                {'error': 'Votre compte est désactivé'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Connecter l'utilisateur
        login(request, user)
        user.seConnecter()
        
        # Récupérer ou créer le token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'role': user.role
        })


class LogoutView(APIView):
    """Déconnexion d'un utilisateur"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Supprimer le token
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Déconnexion réussie'})


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Profil de l'utilisateur connecté"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """Changer le mot de passe"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Vérifier l'ancien mot de passe
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': 'Mot de passe incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mettre à jour le mot de passe
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Mot de passe modifié avec succès'})


# ==================== GESTION DES UTILISATEURS ====================

class UserListView(generics.ListAPIView):
    """Liste de tous les utilisateurs (admin uniquement)"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Détail d'un utilisateur"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response(
                {'error': 'Vous ne pouvez pas supprimer votre propre compte'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().delete(request, *args, **kwargs)


class ActivateUserView(APIView):
    """Activer un utilisateur (admin uniquement)"""
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            user.is_actif = True
            user.save()
            return Response({'message': 'Utilisateur activé avec succès'})
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'Utilisateur non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )


class DeactivateUserView(APIView):
    """Désactiver un utilisateur (admin uniquement)"""
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            if user == request.user:
                return Response(
                    {'error': 'Vous ne pouvez pas désactiver votre propre compte'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.is_actif = False
            user.save()
            return Response({'message': 'Utilisateur désactivé avec succès'})
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'Utilisateur non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )


class VerifyUserView(APIView):
    """Vérifier un utilisateur (admin uniquement)"""
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            user.is_verified = True
            user.save()
            return Response({'message': 'Utilisateur vérifié avec succès'})
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'Utilisateur non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )


# ==================== VIEWSETS ====================

class PassagerViewSet(viewsets.ModelViewSet):
    """CRUD pour les passagers"""
    queryset = Passager.objects.all()
    serializer_class = PassagerSerializer
    permission_classes = [IsAdminOrSelf]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Passager.objects.all()
        return Passager.objects.filter(utilisateur=self.request.user)


class TransporteurViewSet(viewsets.ModelViewSet):
    """CRUD pour les transporteurs"""
    queryset = Transporteur.objects.all()
    serializer_class = TransporteurSerializer
    permission_classes = [IsAdminOrSelf]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Transporteur.objects.all()
        return Transporteur.objects.filter(utilisateur=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)


class AdministrateurViewSet(viewsets.ModelViewSet):
    """CRUD pour les administrateurs"""
    queryset = Administrateur.objects.all()
    serializer_class = AdministrateurSerializer
    permission_classes = [IsAdmin]