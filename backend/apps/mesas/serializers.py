from rest_framework import serializers
from .models import Mesa
from usuarios.serializers import UsuarioSerializer  

class MesaSerializer(serializers.ModelSerializer):
    mesero_asignado_info = UsuarioSerializer(source='mesero_asignado', read_only=True)

    class Meta:
        model = Mesa
        fields = [
            'id',
            'numero',
            'capacidad',
            'estado',
            'mesero_asignado',
            'mesero_asignado_info',
            'creada_en',
            'actualizada_en',
        ]
