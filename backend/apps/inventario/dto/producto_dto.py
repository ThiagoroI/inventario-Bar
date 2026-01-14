from rest_framework import serializers
from apps.inventario.models import Producto  

class ProductoDTO(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'cantidad_nominal', 'unidad', 'precio', 'stock']
