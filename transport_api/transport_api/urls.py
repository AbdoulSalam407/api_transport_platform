from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.auth_urls")),
    path("api/", include("users.urls")),
    path("api/", include("vehicules.urls")),
    path("api/", include("trajets.urls")),
    path("api/", include("reservations.urls")),
    path("api/", include("paiements.urls")),
    path("api/", include("notifications.urls")),
]
