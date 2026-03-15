"""
Permissions personnalisées pour l'API
"""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission : Admin peut modifier, tous le reste peut lire"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission : Le propriétaire peut modifier son objet, autres peuvent lire"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsClient(permissions.BasePermission):
    """Permission : L'utilisateur doit être un client"""
    
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'role') and request.user.role == 'client'


class IsDriver(permissions.BasePermission):
    """Permission : L'utilisateur doit être un chauffeur"""
    
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'role') and request.user.role == 'driver'
