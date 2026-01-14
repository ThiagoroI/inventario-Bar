# usuarios/serializers.py
from rest_framework import serializers
from apps.usuarios.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Usuario.
    Devuelve id, username, email, role y permite crear usuarios con contraseña encriptada.
    """
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # No mostrar la contraseña al devolver datos
        }

    def create(self, validated_data):
        # Extraer la contraseña antes de crear el usuario
        password = validated_data.pop('password', None)
        user = Usuario(**validated_data)
        if password:
            user.set_password(password)  # 🔒 Encripta la contraseña
        user.save()
        return user
