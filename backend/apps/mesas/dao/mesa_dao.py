from apps.mesas.models import Mesa

class MesaDAO:
    """
    Clase DAO (Data Access Object) para encapsular la lógica de acceso
    a la base de datos de las mesas.
    """

    @staticmethod
    def obtener_todas():
        return Mesa.objects.all().order_by('numero')

    @staticmethod
    def obtener_por_id(mesa_id):
        try:
            return Mesa.objects.get(id=mesa_id)
        except Mesa.DoesNotExist:
            return None

    @staticmethod
    def crear_mesa(datos):
        return Mesa.objects.create(**datos)

    @staticmethod
    def actualizar_estado(mesa, nuevo_estado):
        mesa.estado = nuevo_estado
        mesa.save()
        return mesa

    @staticmethod
    def asignar_mesero(mesa, mesero):
        mesa.mesero_asignado = mesero
        mesa.estado = 'ocupada'
        mesa.save()
        return mesa
