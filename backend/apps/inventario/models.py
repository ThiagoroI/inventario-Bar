from django.db import models

class Producto(models.Model):
    UNIDADES = [
        ('ML', 'mililitros'),
        ('L', 'litros'),
    ]

    nombre = models.CharField(max_length=100)
    cantidad_nominal = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=2, choices=UNIDADES, default='ML')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} - {self.cantidadNominal}{self.unidad}"