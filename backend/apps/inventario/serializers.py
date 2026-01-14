from rest_framework import serializers
from apps.inventario.models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'cantidad_nominal',
            'unidad',
            'precio',
            'stock'
        ]
