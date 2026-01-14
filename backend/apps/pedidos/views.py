from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied, ValidationError

from .models import Pedido
from .serializers import PedidoSerializer

from apps.pedidos.dto.pedido_dto import PedidoDTO, DetallePedidoDTO
from apps.pedidos.services.pedido_service import PedidoService


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    # ----------------------------------
    # CREATE usando el DTO + Service
    # ----------------------------------
    def create(self, request, *args, **kwargs):
        try:
            detalles_dto = [
                DetallePedidoDTO(
                    producto_id=detalle.get("producto_id"),
                    cantidad=detalle.get("cantidad")
                )
                for detalle in request.data.get("detalles", [])
            ]

            pedido_dto = PedidoDTO(
                mesa_id=request.data.get("mesa_id"),
                detalles=detalles_dto
            )

            pedido = PedidoService.crear_pedido(pedido_dto, request.user)
            serializer = PedidoSerializer(pedido)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except (ValidationError, PermissionDenied) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ----------------------------------
    # LISTAR POR ROL
    # GET /api/pedidos/listar/
    # ----------------------------------
    @action(detail=False, methods=['get'])
    def listar(self, request):
        pedidos = PedidoService.ver_pedidos(request.user)
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    # ----------------------------------
    # PEDIDOS PARA CAJERO
    # GET /api/pedidos/cajero/
    # ----------------------------------
    @action(detail=False, methods=['get'])
    def cajero(self, request):
        if request.user.role not in ["cajero", "admin"]:
            return Response({"error": "No autorizado"}, status=403)

        pedidos = PedidoService.ver_pedidos_pendientes_pago()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    # ----------------------------------
    # PEDIDOS DE MESERO
    # GET /api/pedidos/mesero/
    # ----------------------------------
    @action(detail=False, methods=['get'])
    def mesero(self, request):
        if request.user.role not in ["mesero", "admin"]:
            return Response({"error": "No autorizado"}, status=403)

        pedidos = PedidoService.ver_pedidos_de_mesero(request.user)
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    # ----------------------------------
    # ACTUALIZAR ESTADO
    # PATCH /api/pedidos/<id>/estado/
    # ----------------------------------
    @action(detail=True, methods=['patch'])
    def estado(self, request, pk=None):
        nuevo_estado = request.data.get("estado")

        if not nuevo_estado:
            return Response({"error": "Debes indicar un estado"}, status=400)

        try:
            pedido = PedidoService.actualizar_estado(request.user, pk, nuevo_estado)
            serializer = PedidoSerializer(pedido)
            return Response(serializer.data)

        except PermissionDenied as e:
            return Response({"error": str(e)}, status=403)
