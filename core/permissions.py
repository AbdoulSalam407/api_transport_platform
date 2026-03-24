"""
Permissions personnalisées pour l'API Transport Platform
"""

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Permission pour les administrateurs"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )
    
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )


class IsTransporteur(permissions.BasePermission):
    """Permission pour les transporteurs"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.role == 'transporteur'
        )
    
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and (
            request.user.role == 'transporteur'
        )


class IsPassager(permissions.BasePermission):
    """Permission pour les passagers"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.role == 'passager'
        )


class IsAdminOrSelf(permissions.BasePermission):
    """Permission: admin ou l'utilisateur lui-même"""
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Admin a tous les droits
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        
        # Vérifier si c'est l'utilisateur lui-même
        if hasattr(obj, 'utilisateur'):
            return obj.utilisateur == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'id') and hasattr(request.user, 'id'):
            # Si c'est directement un objet utilisateur
            return obj == request.user
        
        return False


class IsAdminOrTransporteur(permissions.BasePermission):
    """Permission: admin ou transporteur"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'admin' or request.user.role == 'transporteur'
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.role == 'transporteur':
            # Vérifier si l'objet appartient au transporteur
            if hasattr(obj, 'transporteur'):
                return obj.transporteur.utilisateur == request.user
            if hasattr(obj, 'utilisateur') and hasattr(obj.utilisateur, 'transporteur_profile'):
                return obj.utilisateur == request.user
            return True
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission: admin a tous les droits, les autres seulement en lecture"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Permission: lecture publique, écriture réservée aux authentifiés"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated