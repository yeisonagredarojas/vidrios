"""
Modelo de Trabajadores.
"""
from django.db import models


class Trabajador(models.Model):
    ROL = [
        ('cortador', 'Cortador de vidrio'),
        ('instalador', 'Instalador'),
        ('diseñador', 'Diseñador / Tallador'),
        ('vendedor', 'Vendedor'),
        ('administrador', 'Administrador'),
        ('conductor', 'Conductor / Mensajero'),
    ]

    nombre = models.CharField(max_length=200, verbose_name="Nombre completo")
    rol = models.CharField(max_length=30, choices=ROL, verbose_name="Rol")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    correo = models.EmailField(blank=True, null=True)
    usuario = models.OneToOneField(
        'auth.User', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='trabajador',
        verbose_name="Usuario del sistema"
    )
    activo = models.BooleanField(default=True)
    fecha_ingreso = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_rol_display()})"
