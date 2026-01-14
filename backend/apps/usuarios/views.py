from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.usuarios.models import Usuario
from apps.usuarios.serializers import UsuarioSerializer
from apps.usuarios.dao.usuario_dao import UsuarioDAO


# =====================================================
#   SERIALIZER PERSONALIZADO PARA LOGIN JWT
# =====================================================
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Agregar información del usuario al response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role
        }
        return data


# =====================================================
#   LOGIN - JWT
# =====================================================
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


# =====================================================
#   INFORMACIÓN DEL USUARIO AUTENTICADO (JWT)
# =====================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    usuario_id = request.user.id
    usuario = UsuarioDAO.obtener_usuario_por_id(usuario_id)

    if not usuario:
        return Response({"error": "Usuario no encontrado"}, status=404)

    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)


# =====================================================
#   CRUD DEL USUARIO (ADMIN)
# =====================================================
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


# =====================================================
#   ADMIN TASKS
# =====================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_tasks(request):
    if request.user.role != 'admin':
        return Response({"error": "No autorizado"}, status=403)

    return Response({
        "tasks": [
            "Gestionar usuarios",
            "Ver reportes",
            "Configurar sistema",
            "Administrar inventario",
            "Controlar mesas y pedidos",
            "Configurar roles y permisos"
        ]
    })


# =====================================================
#   MESERO TASKS
# =====================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mesero_tasks(request):
    if request.user.role != 'mesero':
        return Response({"error": "No autorizado"}, status=403)

    return Response({
        "tasks": [
            "Tomar pedidos",
            "Seleccionar mesa",
            "Buscar el producto",
            "Inventario en línea",
            "Actualizar estado de la mesa",
            "Modificar pedido"
        ]
    })


# =====================================================
#   CAJERO TASKS
# =====================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cajero_tasks(request):
    if request.user.role != 'cajero':
        return Response({"error": "No autorizado"}, status=403)

    return Response({
        "tasks": [
            "Cancelar pedido",
            "Ver pedido",
            "Método de pago: Tarjeta crédito, Tarjeta débito, Efectivo"
        ]
    })
