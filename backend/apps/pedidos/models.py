from django.db import models
from django.conf import settings
from apps.mesas.models import Mesa
from apps.inventario.models import Producto
from decimal import Decimal

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]

    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name="pedidos")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa.numero} ({self.estado})"

    def actualizar_total(self):
        """Recalcula el total del pedido basado en los detalles."""
        total = sum(det.subtotal for det in self.detalles.all())
        self.total = total
        self.save(update_fields=["total"])
        return self.total


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido {self.pedido.id})"

    def save(self, *args, **kwargs):
        # Calcula el subtotal antes de guardar
        self.subtotal = Decimal(self.producto.precio) * Decimal(self.cantidad)
        super().save(*args, **kwargs)

        # Después de guardar, actualiza el total del pedido
        self.pedido.actualizar_total()
