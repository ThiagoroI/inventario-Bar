# apps/pedidos/dao/pedido_dao.py
from django.db import transaction
from django.db.models import Sum, F
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from apps.pedidos.models import Pedido, DetallePedido
from apps.inventario.models import Producto
from apps.mesas.models import Mesa
from apps.usuarios.models import Usuario  # <- ahora coincide con UsuarioSerializer


class PedidoDAO:

    # -----------------------------------------------------------
    # CREAR PEDIDO
    # -----------------------------------------------------------
    @staticmethod
    @transaction.atomic
    def crear_pedido(pedido_dto):
        """
        Crea un pedido junto con sus detalles usando DTOs validados.

        Reglas:
        - La mesa debe existir.
        - Debe estar disponible (sin pedidos pendientes/en proceso).
        - Se marca como 'ocupada' al generar un pedido.
        - Se calcula el total automáticamente.
        """

        # -----------------------------------------------------------
        # VALIDAR USUARIO
        # -----------------------------------------------------------
        try:
            usuario = Usuario.objects.get(id=pedido_dto.usuario_id)
        except Usuario.DoesNotExist:
            raise ValidationError(f"Usuario con id {pedido_dto.usuario_id} no existe")

        # -----------------------------------------------------------
        # VALIDAR MESA
        # -----------------------------------------------------------
        try:
            mesa = Mesa.objects.get(id=pedido_dto.mesa_id)
        except Mesa.DoesNotExist:
            raise ValidationError(f"Mesa con id {pedido_dto.mesa_id} no existe")

        # Verificar si tiene pedido activo
        pedido_activo = Pedido.objects.filter(
            mesa=mesa,
            estado__in=["pendiente", "en_proceso"]
        ).exists()

        if pedido_activo:
            raise ValidationError(f"La mesa {mesa.numero} ya tiene un pedido activo.")

        # -----------------------------------------------------------
        # CREAR EL PEDIDO BASE
        # -----------------------------------------------------------
        pedido = Pedido.objects.create(
            mesa=mesa,
            usuario=usuario,
            estado="pendiente",
            total=0
        )

        # -----------------------------------------------------------
        # CREAR DETALLES
        # -----------------------------------------------------------
        total = 0

        for detalle_dto in pedido_dto.detalles:

            # Validar producto
            try:
                producto = Producto.objects.get(id=detalle_dto.producto_id)
            except Producto.DoesNotExist:
                raise ValidationError(f"Producto con id {detalle_dto.producto_id} no existe")

            cantidad = int(detalle_dto.cantidad)

            # Calcular subtotal
            subtotal = producto.precio * cantidad

            # Crear detalle
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                subtotal=subtotal
            )

            total += subtotal

        # Actualizar total
        pedido.total = total
        pedido.save()

        # -----------------------------------------------------------
        # MARCAR MESA COMO OCUPADA
        # -----------------------------------------------------------
        if mesa.estado != "ocupada":
            mesa.estado = "ocupada"
            mesa.save(update_fields=["estado"])

        return pedido

    # -----------------------------------------------------------
    # OBTENER PEDIDO POR ID
    # -----------------------------------------------------------
    @staticmethod
    def obtener_pedido_por_id(pedido_id):
        """
        Retorna un pedido con mesa, usuario y detalles optimizados.
        """
        return (
            Pedido.objects
            .select_related("mesa", "usuario")
            .prefetch_related("detalles__producto")
            .get(id=pedido_id)
        )

    # -----------------------------------------------------------
    # ACTUALIZAR ESTADO DEL PEDIDO
    # -----------------------------------------------------------
    @staticmethod
    def actualizar_estado(pedido_id, nuevo_estado):
        """
        Cambia el estado del pedido y libera la mesa si corresponde.
        """
        pedido = Pedido.objects.select_related("mesa").get(id=pedido_id)
        pedido.estado = nuevo_estado
        pedido.save()

        # Si finaliza, liberar mesa
        if nuevo_estado in ["pagado", "cancelado"]:
            mesa = pedido.mesa
            otros_activos = Pedido.objects.filter(
                mesa=mesa,
                estado__in=["pendiente", "en_proceso"]
            ).exclude(id=pedido.id).exists()

            if not otros_activos and mesa.estado != "disponible":
                mesa.estado = "disponible"
                mesa.save(update_fields=["estado"])

        return pedido

    # -----------------------------------------------------------
    # ELIMINAR PEDIDO
    # -----------------------------------------------------------
    @staticmethod
    def eliminar_pedido(pedido_id):
        """
        Elimina un pedido y sus detalles.  
        Si no quedan pedidos activos en la mesa → se libera.
        """
        pedido = Pedido.objects.select_related("mesa").get(id=pedido_id)
        mesa = pedido.mesa

        pedido.delete()

        otros_activos = Pedido.objects.filter(
            mesa=mesa,
            estado__in=["pendiente", "en_proceso"]
        ).exists()

        if not otros_activos and mesa.estado != "disponible":
            mesa.estado = "disponible"
            mesa.save(update_fields=["estado"])

    # -----------------------------------------------------------
    # LISTAR PEDIDOS PARA CAJERO
    # -----------------------------------------------------------
    @staticmethod
    def obtener_pedidos_cajero():
        """
        Retorna los pedidos activos con totales calculados.
        """
        return (
            Pedido.objects
            .filter(estado__in=["pendiente", "en_proceso"])
            .annotate(
                total=Sum(F("detalles__cantidad") * F("detalles__producto__precio"))
            )
            .select_related("mesa", "usuario")
            .prefetch_related("detalles__producto")
        )
