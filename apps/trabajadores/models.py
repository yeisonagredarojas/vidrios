from django.db import models


class Trabajador(models.Model):
    ROL = [
        ('cortador','Cortador'),('instalador','Instalador'),
        ('disenador','Disenador'),('vendedor','Vendedor'),
        ('administrador','Administrador'),('conductor','Conductor'),
    ]
    nombre       = models.CharField(max_length=200)
    rol          = models.CharField(max_length=30, choices=ROL)
    telefono     = models.CharField(max_length=20)
    correo       = models.EmailField(blank=True, null=True)
    activo       = models.BooleanField(default=True)
    fecha_ingreso= models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.rol})"
