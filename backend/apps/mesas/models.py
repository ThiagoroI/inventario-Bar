from django.db import models
from django.conf import settings  # para referirnos al modelo Usuario personalizado

class Mesa(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada'),
    ]

    numero = models.PositiveIntegerField(unique=True)
    capacidad = models.PositiveIntegerField(default=4)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='disponible')

    # mesero tiene asignada la mesa actualmente
    mesero_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL,        
        on_delete=models.SET_NULL,      
        null=True, blank=True,
        related_name='mesas_asignadas'
    )

    # Para tener un control de tiempo
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mesa {self.numero} ({self.estado})"
