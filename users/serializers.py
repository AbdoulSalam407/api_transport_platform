from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Passager, Transporteur, Administrateur


class UserSerializer(serializers.ModelSerializer):
    """Sérializer de base pour CustomUser"""
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'nom', 'prenom', 'role',
            'telephone', 'is_verified', 'is_actif', 'date_inscription',
            'photo', 'last_login'
        ]
        read_only_fields = ['id', 'date_inscription', 'last_login', 'is_verified']


class UserCreateSerializer(serializers.ModelSerializer):
    """Sérializer pour la création d'utilisateur"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    # Champs spécifiques pour transporteur
    nom_entreprise = serializers.CharField(required=False, allow_blank=True)
    numero_licence = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'nom', 'prenom', 'role', 'telephone',
            'nom_entreprise', 'numero_licence'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        
        # Vérifications pour transporteur
        if attrs.get('role') == 'transporteur':
            if not attrs.get('nom_entreprise'):
                raise serializers.ValidationError({"nom_entreprise": "Le nom de l'entreprise est requis pour un transporteur."})
            if not attrs.get('numero_licence'):
                raise serializers.ValidationError({"numero_licence": "Le numéro de licence est requis pour un transporteur."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        nom_entreprise = validated_data.pop('nom_entreprise', None)
        numero_licence = validated_data.pop('numero_licence', None)
        
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nom=validated_data['nom'],
            prenom=validated_data['prenom'],
            role=validated_data['role'],
            telephone=validated_data.get('telephone', '')
        )
        
        # Créer le profil selon le rôle
        if user.role == 'passager':
            Passager.objects.create(utilisateur=user)
        elif user.role == 'transporteur':
            Transporteur.objects.create(
                utilisateur=user,
                nom_entreprise=nom_entreprise,
                numero_licence=numero_licence
            )
        elif user.role == 'admin':
            Administrateur.objects.create(utilisateur=user)
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Sérializer pour le profil utilisateur"""
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'nom', 'prenom', 'role',
            'telephone', 'photo', 'is_verified', 'is_actif'
        ]
        read_only_fields = ['id', 'role', 'is_verified', 'is_actif']


class LoginSerializer(serializers.Serializer):
    """Sérializer pour la connexion"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """Sérializer pour le changement de mot de passe"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Les mots de passe ne correspondent pas."})
        return attrs


class PassagerSerializer(serializers.ModelSerializer):
    """Sérializer pour Passager"""
    utilisateur = UserSerializer(read_only=True)
    utilisateur_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='utilisateur',
        write_only=True
    )
    nom_complet = serializers.SerializerMethodField()
    
    class Meta:
        model = Passager
        fields = [
            'utilisateur', 'utilisateur_id', 'preferences_siege',
            'notifications_activees', 'points_fidelite', 'nom_complet'
        ]
    
    def get_nom_complet(self, obj):
        return f"{obj.utilisateur.nom} {obj.utilisateur.prenom}"


class TransporteurSerializer(serializers.ModelSerializer):
    """Sérializer pour Transporteur"""
    utilisateur = UserSerializer(read_only=True)
    utilisateur_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='utilisateur',
        write_only=True
    )
    nom_complet = serializers.SerializerMethodField()
    nombre_vehicules = serializers.SerializerMethodField()
    
    class Meta:
        model = Transporteur
        fields = [
            'utilisateur', 'utilisateur_id', 'nom_entreprise',
            'numero_licence', 'verifie', 'note_moyenne',
            'logo', 'est_ouvert', 'nom_complet', 'nombre_vehicules'
        ]
    
    def get_nom_complet(self, obj):
        return f"{obj.utilisateur.nom} {obj.utilisateur.prenom}"
    
    def get_nombre_vehicules(self, obj):
        return obj.vehicules.count()


class AdministrateurSerializer(serializers.ModelSerializer):
    """Sérializer pour Administrateur"""
    utilisateur = UserSerializer(read_only=True)
    utilisateur_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='utilisateur',
        write_only=True
    )
    
    class Meta:
        model = Administrateur
        fields = ['utilisateur', 'utilisateur_id', 'niveau_acces']