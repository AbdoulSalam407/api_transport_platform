from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import MeView, UserViewSet

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
] + router.urls
