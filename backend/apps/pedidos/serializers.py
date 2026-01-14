from rest_framework import serializers
from apps.pedidos.models import Pedido, DetallePedido
from apps.inventario.models import Producto
from apps.mesas.models import Mesa


    # =======================
    #   DETALLE PEDIDO
    # =======================
class DetallePedidoSerializer(serializers.ModelSerializer):
        producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
        producto_precio = serializers.DecimalField(source="producto.precio", read_only=True,
                                                max_digits=10, decimal_places=2)

        class Meta:
            model = DetallePedido
            fields = [
                "id",
                "producto",
                "producto_nombre",
                "producto_precio",
                "cantidad",
                "subtotal",
            ]


    # =======================
    #       PEDIDO
    # =======================
class PedidoSerializer(serializers.ModelSerializer):
        mesa_numero = serializers.IntegerField(source="mesa.numero", read_only=True)
        usuario_username = serializers.CharField(source="usuario.username", read_only=True)
        detalles = DetallePedidoSerializer(many=True, read_only=True)

        class Meta:
            model = Pedido
            fields = [
                "id",
                "mesa",
                "mesa_numero",
                "usuario",
                "usuario_username",
                "estado",
                "fecha_creacion",
                "total",
                "detalles"
            ]
            read_only_fields = ["usuario", "total", "fecha_creacion"]
