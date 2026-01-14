from django.core.exceptions import PermissionDenied
from apps.pedidos.models import Pedido, DetallePedido
from apps.mesas.models import Mesa
from apps.inventario.models import Producto


class PedidoService:

    # --------------------------------------------------------
    # CREAR PEDIDO
    # --------------------------------------------------------
    @staticmethod
    def crear_pedido(dto, usuario):
        # Roles permitidos
        if usuario.role not in ["mesero", "admin"]:
            raise PermissionDenied("No tienes permiso para crear pedidos")

        # Validar mesa
        try:
            mesa = Mesa.objects.get(id=dto.mesa_id)
        except Mesa.DoesNotExist:
            raise PermissionDenied("La mesa no existe")

        # Crear pedido
        pedido = Pedido.objects.create(
            mesa=mesa,
            usuario=usuario,
            estado="pendiente"
        )

        # Crear detalles del pedido
        for d in dto.detalles:
            try:
                producto = Producto.objects.get(id=d.producto_id)
            except Producto.DoesNotExist:
                raise PermissionDenied(f"Producto con id {d.producto_id} no existe")

            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=d.cantidad
            )

        return pedido

    # --------------------------------------------------------
    # VER PEDIDOS GENERAL (POR ROL)
    # --------------------------------------------------------
    @staticmethod
    def ver_pedidos(usuario):
        if usuario.role == "admin":
            return Pedido.objects.all()

        if usuario.role == "mesero":
            return Pedido.objects.filter(usuario=usuario)

        if usuario.role == "cajero":
            return Pedido.objects.filter(estado__in=["pendiente", "en_proceso"])

        raise PermissionDenied("Rol no autorizado para ver pedidos")

    # --------------------------------------------------------
    # PEDIDOS PARA CAJERO
    # --------------------------------------------------------
    @staticmethod
    def ver_pedidos_pendientes_pago():
        return Pedido.objects.filter(estado__in=["pendiente", "en_proceso"])

    # --------------------------------------------------------
    # PEDIDOS DE UN MESERO
    # --------------------------------------------------------
    @staticmethod
    def ver_pedidos_de_mesero(usuario):
        return Pedido.objects.filter(usuario=usuario)

    # --------------------------------------------------------
    # ACTUALIZAR ESTADO DE PEDIDO
    # --------------------------------------------------------
    @staticmethod
    def actualizar_estado(usuario, pedido_id, nuevo_estado):
        try:
            pedido = Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            raise PermissionDenied("Pedido no encontrado")

        # Solo admin o el dueño puede actualizar
        if usuario.role not in ["admin", "mesero"]:
            raise PermissionDenied("No tienes permiso para cambiar el estado")

        if usuario.role == "mesero" and pedido.usuario != usuario:
            raise PermissionDenied("Solo el mesero que creó el pedido puede cambiar su estado")

        pedido.estado = nuevo_estado
        pedido.save()
        return pedido

    # --------------------------------------------------------
    # ELIMINAR PEDIDO
    # --------------------------------------------------------
    @staticmethod
    def eliminar_pedido(usuario, pedido_id):
        if usuario.role != "admin":
            raise PermissionDenied("Solo el administrador puede eliminar pedidos")

        try:
            pedido = Pedido.objects.get(id=pedido_id)
            pedido.delete()
        except Pedido.DoesNotExist:
            raise PermissionDenied("Pedido no encontrado")

    # --------------------------------------------------------
    # DETALLE DE PEDIDO
    # --------------------------------------------------------
    @staticmethod
    def obtener_detalle_pedido(usuario, pedido_id):
        try:
            pedido = Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            raise PermissionDenied("Pedido no encontrado")

        if usuario.role == "mesero" and pedido.usuario != usuario:
            raise PermissionDenied("No tienes permiso para ver este pedido")

        return pedido
