from rest_framework import serializers
from apps.mesas.models import Mesa

class MesaSerializer(serializers.ModelSerializer):
    mesero_nombre = serializers.CharField(source='mesero_asignado.username', read_only=True)

    class Meta:
        model = Mesa
        fields = ['id', 'numero', 'capacidad', 'estado', 'mesero_asignado', 'mesero_nombre']
