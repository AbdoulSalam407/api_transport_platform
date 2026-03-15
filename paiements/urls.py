from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PaiementViewSet

router = SimpleRouter()
router.register(r"", PaiementViewSet, basename="paiement")

urlpatterns = [
    path("", include(router.urls)),
]
