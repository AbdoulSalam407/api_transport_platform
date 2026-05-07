from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaiementViewSet

router = SimpleRouter()
router.register(r"paiements", PaiementViewSet, basename="paiement")

urlpatterns = [
    path("", include(router.urls)),
]
