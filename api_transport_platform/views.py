from django.http import JsonResponse


def api_root(request):
    """Point d'entrée à la racine du site : évite un 404 sur http://localhost:8000/"""
    return JsonResponse(
        {
            "service": "Transport Platform API",
            "message": "Utilisez les préfixes listés ci-dessous (ex. /trajets/).",
            "paths": {
                "admin": "/admin/",
                "users": "/users/",
                "vehicules": "/vehicules/",
                "trajets": "/trajets/",
                "reservations": "/reservations/",
                "paiements": "/paiements/",
                "notifications": "/notifications/",
                "transports": "/transports/",
                "api_auth": "/api-auth/",
                "token_auth": "/api-token-auth/",
                "openapi_schema": "/api/schema/",
                "swagger_ui": "/api/docs/",
            },
        }
    )
