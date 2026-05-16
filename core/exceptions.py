"""
Exceptions et réponses personnalisées
"""
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
import logging

logger = logging.getLogger(__name__)


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


class CustomAPIException(APIException):
    """Exception personnalisée pour l'API"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Erreur API'
    default_code = 'api_error'
    
    def __init__(self, detail=None, code=None, status_code=None):
        if status_code:
            self.status_code = status_code
        super().__init__(detail=detail, code=code)


def custom_exception_handler(exc, context):
    """
    Handler personnalisé pour les exceptions
    Retourne un format cohérent pour toutes les erreurs
    """
    response = exception_handler(exc, context)
    
    # Log les erreurs
    logger.error(f"Exception: {exc}", exc_info=True)
    
    if response is not None:
        # Format cohérent pour les erreurs
        if isinstance(response.data, dict):
            # Si c'est déjà un dictionnaire, on le reformate
            error_detail = response.data.get('detail', str(response.data))
            response.data = {
                'status': 'error',
                'status_code': response.status_code,
                'message': str(error_detail),
                'errors': response.data
            }
        else:
            # Si c'est une liste ou autre format
            response.data = {
                'status': 'error',
                'status_code': response.status_code,
                'message': str(response.data),
                'errors': response.data
            }
    else:
        # Pour les exceptions non gérées par DRF
        response = Response(
            {
                'status': 'error',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Erreur serveur interne',
                'errors': str(exc)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response

