"""
Modelo de Proveedores.
"""
from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre / Empresa")
    contacto = models.CharField(max_length=200, blank=True, verbose_name="Persona de contacto")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    correo = models.EmailField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True)
    tipo_material = models.CharField(max_length=200, verbose_name="Tipo de material que provee")
    notas = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.tipo_material}"
