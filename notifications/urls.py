from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'notifications', views.NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints spécifiques
    path('mes-notifications/', views.MesNotificationsView.as_view(), name='mes-notifications'),
    path('non-lues/', views.NotificationsNonLuesView.as_view(), name='notifications-non-lues'),
    path('compter/', views.CompterNotificationsNonLuesView.as_view(), name='compter-notifications'),
    path('marquer/<int:pk>/', views.MarquerNotificationLueView.as_view(), name='marquer-notification'),
    path('marquer-lues/', views.MarquerNotificationsLuesView.as_view(), name='marquer-notifications'),
    path('supprimer/<int:pk>/', views.SupprimerNotificationView.as_view(), name='supprimer-notification'),
    path('supprimer-toutes/', views.SupprimerToutesNotificationsView.as_view(), name='supprimer-toutes'),
    path('creer/', views.CreerNotificationView.as_view(), name='creer-notification'),
    path('trajet/<int:trajet_id>/notifier/', views.NotifierPassagersView.as_view(), name='notifier-passagers'),
]
