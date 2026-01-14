from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.mesas.dao.mesa_dao import MesaDAO
from apps.mesas.dto.mesa_dto import MesaSerializer
from apps.mesas.models import Mesa
from apps.usuarios.models import Usuario


class MesaViewSet(viewsets.ViewSet):
    """
    ViewSet para manejar las operaciones sobre las mesas usando MesaDAO.
    """

    permission_classes = [IsAuthenticated]

    # ----------------------------------
    # GET /api/mesas/
    # ----------------------------------
    def list(self, request):
        mesas = MesaDAO.obtener_todas()
        serializer = MesaSerializer(mesas, many=True)
        return Response(serializer.data)

    # ----------------------------------
    # GET /api/mesas/{id}/
    # ----------------------------------
    def retrieve(self, request, pk=None):
        mesa = MesaDAO.obtener_por_id(pk)
        if not mesa:
            return Response({"error": "Mesa no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MesaSerializer(mesa)
        return Response(serializer.data)

    # ----------------------------------
    # POST /api/mesas/
    # ----------------------------------
    def create(self, request):
        serializer = MesaSerializer(data=request.data)
        if serializer.is_valid():
            mesa = MesaDAO.crear_mesa(serializer.validated_data)
            return Response(MesaSerializer(mesa).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ----------------------------------
    # PUT /api/mesas/{id}/
    # ----------------------------------
    def update(self, request, pk=None):
        mesa = MesaDAO.obtener_por_id(pk)

        if not mesa:
            return Response({"error": "Mesa no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MesaSerializer(mesa, data=request.data, partial=False)
        if serializer.is_valid():
            MesaDAO.actualizar_mesa(mesa, serializer.validated_data)
            return Response(MesaSerializer(mesa).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ----------------------------------
    # PATCH /api/mesas/{id}/
    # ----------------------------------
    def partial_update(self, request, pk=None):
        mesa = MesaDAO.obtener_por_id(pk)

        if not mesa:
            return Response({"error": "Mesa no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MesaSerializer(mesa, data=request.data, partial=True)
        if serializer.is_valid():
            MesaDAO.actualizar_mesa(mesa, serializer.validated_data)
            return Response(MesaSerializer(mesa).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ----------------------------------
    # DELETE /api/mesas/{id}/
    # ----------------------------------
    def destroy(self, request, pk=None):
        mesa = MesaDAO.obtener_por_id(pk)

        if not mesa:
            return Response({"error": "Mesa no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        MesaDAO.eliminar_mesa(mesa)
        return Response({"message": "Mesa eliminada"}, status=status.HTTP_204_NO_CONTENT)

    # ----------------------------------
    # POST /api/mesas/{id}/asignar_mesero/
    # ----------------------------------
    @action(detail=True, methods=["post"])
    def asignar_mesero(self, request, pk=None):
        mesa = MesaDAO.obtener_por_id(pk)
        if not mesa:
            return Response({"error": "Mesa no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        mesero_id = request.data.get("mesero_id")
        if not mesero_id:
            return Response({"error": "Debe enviar el ID del mesero"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mesero = Usuario.objects.get(id=mesero_id, rol="mesero")
        except Usuario.DoesNotExist:
            return Response({"error": "Mesero no válido"}, status=status.HTTP_400_BAD_REQUEST)

        MesaDAO.asignar_mesero(mesa, mesero)

        return Response(MesaSerializer(mesa).data, status=status.HTTP_200_OK)

    # ----------------------------------
    # POST /api/mesas/{id}/liberar/
    # ----------------------------------
    @action(detail=True, methods=["post"])
    def liberar(self, request, pk=None):
        mesa = MesaDAO.obtener_por_id(pk)
        if not mesa:
            return Response({"error": "Mesa no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        # Estado correcto según tu modelo
        MesaDAO.actualizar_estado(mesa, "disponible")
        mesa.mesero_asignado = None
        mesa.save()

        return Response(MesaSerializer(mesa).data, status=status.HTTP_200_OK)
