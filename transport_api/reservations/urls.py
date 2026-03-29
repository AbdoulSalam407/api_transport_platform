from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ReservationViewSet

router = SimpleRouter()
router.register(r"reservations", ReservationViewSet, basename="reservation")

urlpatterns = [
    path("", include(router.urls)),
]
