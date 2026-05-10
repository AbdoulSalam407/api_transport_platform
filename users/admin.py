from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Passager, Transporteur, Administrateur

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'nom', 'prenom', 'role', 'is_actif', 'is_verified')
    list_filter = ('role', 'is_actif', 'is_verified')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'telephone', 'photo')}),
        ('Rôle et statut', {'fields': ('role', 'is_verified', 'is_actif')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Passager)
admin.site.register(Transporteur)
admin.site.register(Administrateur)