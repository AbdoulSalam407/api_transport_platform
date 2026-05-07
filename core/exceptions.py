"""
Exceptions et réponses personnalisées
"""
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Erreur de validation.'
    default_code = 'invalid'


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Ressource non trouvée.'
    default_code = 'not_found'


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Accès refusé.'
    default_code = 'permission_denied'


def custom_exception_handler(exc, context):
    """Handler personnalisé pour les exceptions"""
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data['status_code'] = response.status_code
    
    return response

