from rest_framework import serializers
from apps.usuarios.models import Usuario

# ===============================================
# Serializer para el modelo Usuario
# Se encarga de convertir objetos Usuario en JSON y viceversa,
# además de manejar la creación y actualización de usuarios
# ===============================================
class UsuarioSerializer(serializers.ModelSerializer):
    # El campo password se define como solo escritura (write_only)
    # Esto evita que la contraseña se muestre al obtener datos del usuario
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        # Modelo asociado
        model = Usuario
        # Campos que se serializan/deserializan
        fields = ['id', 'username', 'email', 'role', 'password']

    # ================================
    # Método para crear un nuevo usuario
    # ================================
    def create(self, validated_data):
        # Extraemos la contraseña del diccionario de datos validados
        password = validated_data.pop('password')
        # Creamos una instancia de Usuario con los datos restantes
        user = Usuario(**validated_data)
        # Encriptamos la contraseña usando set_password
        user.set_password(password)
        # Guardamos el usuario en la base de datos
        user.save()
        return user

    # ================================
    # Método para actualizar un usuario existente
    # ================================
    def update(self, instance, validated_data):
        # Extraemos la contraseña si se proporciona; si no, queda None
        password = validated_data.pop('password', None)
        # Actualizamos los demás campos del usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # Si se proporcionó una contraseña, la encriptamos
        if password:
            instance.set_password(password)
        # Guardamos los cambios en la base de datos
        instance.save()
        return instanc
