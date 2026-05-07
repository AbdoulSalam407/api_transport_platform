from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'reservations', views.ReservationViewSet)
router.register(r'billets', views.BilletViewSet)
router.register(r'points-ramassage', views.PointRamassageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints spécifiques
    path('creer/', views.CreerReservationView.as_view(), name='creer-reservation'),
    path('mes-reservations/', views.MesReservationsView.as_view(), name='mes-reservations'),
    path('reservations/<int:pk>/confirmer/', views.ConfirmerReservationView.as_view(), name='confirmer-reservation'),
    path('reservations/<int:pk>/annuler/', views.AnnulerReservationView.as_view(), name='annuler-reservation'),
    path('reservations/<int:pk>/recupere/', views.MarquerRecupereView.as_view(), name='marquer-recupere'),
    path('reservations/<int:reservation_id>/generer-billet/', views.GenererBilletView.as_view(), name='generer-billet'),
    path('billets/qr/<str:code_qr>/', views.GenererQRCodeView.as_view(), name='generer-qr'),
    path('reservations/<int:reservation_id>/point-ramassage/', views.DefinirPointRamassageView.as_view(), name='point-ramassage'),
]