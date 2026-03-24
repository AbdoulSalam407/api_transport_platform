from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'paiements', views.PaiementViewSet)
router.register(r'logs', views.TransactionLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints spécifiques
    path('initier/', views.InitierPaiementView.as_view(), name='initier-paiement'),
    path('confirmer/<str:transaction_id>/', views.ConfirmerPaiementView.as_view(), name='confirmer-paiement'),
    path('verifier/<int:pk>/', views.VerifierPaiementView.as_view(), name='verifier-paiement'),
    path('rembourser/<int:pk>/', views.RembourserPaiementView.as_view(), name='rembourser-paiement'),
]