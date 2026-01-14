from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.inventario.models import Producto
from apps.inventario.serializers import ProductoSerializer


class ProductoViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]   # ⬅️ USAR JWT
    permission_classes = [IsAuthenticated]

    # GET /api/productos/
    def list(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # GET /api/productos/<id>/
    def retrieve(self, request, pk=None):
        try:
            producto = Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST /api/productos/
    def create(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT/PATCH /api/productos/<id>/
    def update(self, request, pk=None):
        try:
            producto = Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductoSerializer(
            producto, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /api/productos/<id>/
    def destroy(self, request, pk=None):
        try:
            producto = Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
