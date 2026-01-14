from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.usuarios.views import UsuarioViewSet,  mesero_tasks, cajero_tasks, admin_tasks,user_info
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    # Login
    
    path('user-info/', user_info, name='user-info'),  # ← AQUI
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),


    # Rutas por rol
    path('mesero_tasks/', mesero_tasks, name='mesero_tasks'),
    path('cajero_tasks/', cajero_tasks, name='cajero_tasks'),
    path('admin_tasks/', admin_tasks, name='admin_tasks'),

    # API REST de usuarios
    path('', include(router.urls)),
]

"""
Definicion de endponit:

    También puede referirse a un punto de acceso específico en un servidor al que un cliente API
    se dirige para solicitar y recibir datos o funcionalidades, como una URL.
    
"""