from apps.inventario.models import Producto

class ProductoDAO:
    @staticmethod
    def crear_producto(nombre, cantidad_nominal, unidad, precio, stock):
        return Producto.objects.create(
            nombre=nombre,
            cantidad_nominal=cantidad_nominal,
            unidad = unidad,
            precio=precio,
            stock=stock
        )

    @staticmethod
    def obtener_producto_por_id(producto_id):
        return Producto.objects.filter(id=producto_id).first()

    @staticmethod
    def actualizar_producto(producto_id, **kwargs):
        Producto.objects.filter(id=producto_id).update(**kwargs)
        return Producto.objects.get(id=producto_id)

    @staticmethod
    def eliminar_producto(producto_id):
        return Producto.objects.filter(id=producto_id).delete()

    @staticmethod
    def listar_productos():
        return Producto.objects.all()
