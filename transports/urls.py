from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TransportViewSet

# Create a router and register the ViewSet
router = SimpleRouter()
router.register(r"transports", TransportViewSet, basename="transport")

# URLs will include all router routes
urlpatterns = [
    path("", include(router.urls)),
]
