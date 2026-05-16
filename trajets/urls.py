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
    
    # Nouveaux endpoints dynamiques
    path('mes-trajets/', views.MesTrajetsView.as_view(), name='mes-trajets'),
    path('statistiques/', views.StatistiquesGlobalesView.as_view(), name='statistiques-globales'),
    path('statistiques-transporteur/', views.StatistiquesTransporteurView.as_view(), name='statistiques-transporteur'),
]