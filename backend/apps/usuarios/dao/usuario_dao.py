from apps.usuarios.models import Usuario
from django.contrib.auth.hashers import make_password

class UsuarioDAO:
    """
    DAO para manejar operaciones sobre el modelo Usuario
    """

    @staticmethod
    def crear_usuario(username, email, password, role):
        """
        Crea un nuevo usuario
        """
        usuario = Usuario(
            username=username,
            email=email,
            password=make_password(password),  # cifrar la contraseña
            role=role
        )
        usuario.save()
        return usuario

    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        """
        Obtiene un usuario por su ID
        """
        try:
            return Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def obtener_usuario_por_username(username):
        """
        Obtiene un usuario por su username
        """
        try:
            return Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def listar_usuarios():
        """
        Retorna todos los usuarios
        """
        return Usuario.objects.all()

    @staticmethod
    def actualizar_usuario(usuario_id, **kwargs):
        """
        Actualiza campos de un usuario
        """
        usuario = UsuarioDAO.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return None

        for key, value in kwargs.items():
            if key == "password":
                value = make_password(value)  # cifrar la contraseña
            setattr(usuario, key, value)

        usuario.save()
        return usuario

    @staticmethod
    def eliminar_usuario(usuario_id):
        """
        Elimina un usuario por su ID
        """
        usuario = UsuarioDAO.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return False
        usuario.delete()
        return True

""" 
    es un patrón de diseño que abstrae el acceso a la fuente de datos (como una base de datos), 
    centralizando la lógica de persistencia para operaciones CRUD (crear, leer, actualizar, borrar) 
    y manteniendo la lógica de negocio separada de los detalles de acceso a la base de datos
"""