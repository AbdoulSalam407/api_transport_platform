from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TrajetViewSet

router = SimpleRouter()
router.register(r"trajets", TrajetViewSet, basename="trajet")

urlpatterns = [
    path("", include(router.urls)),
]
