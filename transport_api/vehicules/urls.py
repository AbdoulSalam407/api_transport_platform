from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import VehiculeViewSet

router = SimpleRouter()
router.register(r"vehicules", VehiculeViewSet, basename="vehicule")

urlpatterns = [
    path("", include(router.urls)),
]
