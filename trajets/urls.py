from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TrajetViewSet

router = SimpleRouter()
router.register(r"trajets", TrajetViewSet, basename="trajet")

urlpatterns = [
    path("", include(router.urls)),
]
