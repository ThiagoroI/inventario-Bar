from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.mesas.views import MesaViewSet

router = DefaultRouter()
router.register(r'mesas', MesaViewSet, basename='mesas')

urlpatterns = [
    path('', include(router.urls)),
]
