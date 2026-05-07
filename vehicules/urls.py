from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'marques', views.MarqueViewSet)
router.register(r'modeles', views.ModeleViewSet)
router.register(r'vehicules', views.VehiculeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints spécifiques
    path('vehicules/<int:pk>/disponible/', views.MettreVehiculeDisponibleView.as_view(), name='vehicule-disponible'),
    path('vehicules/<int:pk>/maintenance/', views.MettreVehiculeMaintenanceView.as_view(), name='vehicule-maintenance'),
    path('transporteur/<int:transporteur_id>/vehicules/', views.VehiculesParTransporteurView.as_view(), name='vehicules-transporteur'),
]