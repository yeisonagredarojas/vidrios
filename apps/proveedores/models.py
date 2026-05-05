from django.db import models

class Proveedor(models.Model):
    nombre        = models.CharField(max_length=200)
    contacto      = models.CharField(max_length=200, blank=True)
    telefono      = models.CharField(max_length=20)
    correo        = models.EmailField(blank=True, null=True)
    ciudad        = models.CharField(max_length=100, blank=True)
    tipo_material = models.CharField(max_length=200)
    notas         = models.TextField(blank=True)
    activo        = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
