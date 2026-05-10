from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authtoken_views

# API Root
urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    
    # Authentication
    path("api-auth/", include("rest_framework.urls")),
    path("api-token-auth/", authtoken_views.obtain_auth_token, name="api_token_auth"),
    # API v1
    
    path("users/", include("users.urls")),
    path("vehicules/", include("vehicules.urls")),
    path("trajets/", include("trajets.urls")),
    path("reservations/", include("reservations.urls")),
    path("paiements/", include("paiements.urls")),
    path("notifications/", include("notifications.urls")),
    path("transports/", include("transports.urls")),
        
    ]