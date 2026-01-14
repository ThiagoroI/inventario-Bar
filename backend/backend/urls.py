from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ----------------------
    # RUTAS DE LAS APLICACIONES
    # ----------------------
    path('api/', include('apps.usuarios.urls')),      
    path('api/', include('apps.inventario.urls')),   
    path('api/', include('apps.mesas.urls')),            
    path('api/', include('apps.pedidos.urls')),         
]
