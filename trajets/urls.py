from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'trajets', views.TrajetViewSet)
router.register(r'etapes', views.EtapeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints spécifiques
    path('rechercher/', views.RechercherTrajetView.as_view(), name='rechercher-trajet'),
    path('trajets/<int:pk>/places/', views.VerifierPlacesView.as_view(), name='verifier-places'),
    path('transporteur/<int:transporteur_id>/trajets/', views.TrajetsParTransporteurView.as_view(), name='trajets-transporteur'),
]