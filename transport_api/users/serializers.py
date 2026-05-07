from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Passager, Role, Transporteur, User, ValidationStatut


class PassagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passager
        fields = ("telephone",)


class TransporteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporteur
        fields = ("nom_compagnie", "licence", "statut_validation")
        read_only_fields = ("statut_validation",)


class UserSerializer(serializers.ModelSerializer):
    passager = PassagerSerializer(source="passager_profile", read_only=True, allow_null=True)
    transporteur = TransporteurSerializer(
        source="transporteur_profile", read_only=True, allow_null=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "nom",
            "prenom",
            "role",
            "passager",
            "transporteur",
        )
        read_only_fields = ("id", "role")


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    nom = serializers.CharField(max_length=150)
    prenom = serializers.CharField(max_length=150)
    mot_de_passe = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=Role.choices)
    telephone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    nom_compagnie = serializers.CharField(max_length=200, required=False, allow_blank=True)
    licence = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Cet email est déjà utilisé."})
        role = attrs["role"]
        if role == Role.PASSAGER and not attrs.get("telephone"):
            raise serializers.ValidationError(
                {"telephone": "Requis pour un passager."}
            )
        if role == Role.TRANSPORTEUR:
            if not attrs.get("nom_compagnie") or not attrs.get("licence"):
                raise serializers.ValidationError(
                    "nom_compagnie et licence sont requis pour un transporteur."
                )
        return attrs

    def create(self, validated_data):
        mot_de_passe = validated_data.pop("mot_de_passe")
        role = validated_data.pop("role")
        telephone = validated_data.pop("telephone", "") or ""
        nom_compagnie = validated_data.pop("nom_compagnie", "") or ""
        licence = validated_data.pop("licence", "") or ""

        validate_password(mot_de_passe)
        user = User.objects.create_user(
            password=mot_de_passe,
            role=role,
            **validated_data,
        )
        if role == Role.PASSAGER:
            Passager.objects.create(user=user, telephone=telephone)
        else:
            Transporteur.objects.create(
                user=user,
                nom_compagnie=nom_compagnie,
                licence=licence,
                statut_validation=ValidationStatut.EN_ATTENTE,
            )
        return user
