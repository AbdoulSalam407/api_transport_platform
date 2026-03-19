from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import VehiculeViewSet

router = SimpleRouter()
router.register(r"", VehiculeViewSet, basename="vehicule")

urlpatterns = [
    path("", include(router.urls)),
]
