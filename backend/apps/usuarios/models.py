from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Agregamos los roles
    ADMIN = 'ADMIN'
    MESERO = 'MESERO'
    CAJERO = 'CAJERO'

    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('mesero', 'Mesero'),
        ('cajero', 'Cajero'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='admin')

    def __str__(self):
        return f"{self.username} ({self.role})"
