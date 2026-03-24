from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router pour les ViewSets
router = DefaultRouter()
router.register(r'passagers', views.PassagerViewSet, basename='passager')
router.register(r'transporteurs', views.TransporteurViewSet, basename='transporteur')
router.register(r'administrateurs', views.AdministrateurViewSet, basename='administrateur')

urlpatterns = [
    # Authentification
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    # Utilisateurs
    path('', views.UserListView.as_view(), name='user-list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/activate/', views.ActivateUserView.as_view(), name='activate-user'),
    path('<int:pk>/deactivate/', views.DeactivateUserView.as_view(), name='deactivate-user'),
    path('verify/<int:pk>/', views.VerifyUserView.as_view(), name='verify-user'),
    
    # ViewSets
    path('', include(router.urls)),
]