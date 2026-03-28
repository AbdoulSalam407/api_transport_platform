from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import VehiculeViewSet

router = SimpleRouter()
router.register(r"vehicules", VehiculeViewSet, basename="vehicule")

urlpatterns = [
    path("", include(router.urls)),
]
