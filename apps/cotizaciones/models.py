from django.db import models


class ConfiguracionPrecios(models.Model):
    nombre                    = models.CharField(max_length=100, default='Principal')
    activo                    = models.BooleanField(default=True)
    precio_vidrio_normal_m2   = models.DecimalField(max_digits=10, decimal_places=2, default=25000)
    precio_vidrio_tallado_m2  = models.DecimalField(max_digits=10, decimal_places=2, default=45000)
    precio_espejo_m2          = models.DecimalField(max_digits=10, decimal_places=2, default=35000)
    precio_vidrio_templado_m2 = models.DecimalField(max_digits=10, decimal_places=2, default=80000)
    precio_vidrio_laminado_m2 = models.DecimalField(max_digits=10, decimal_places=2, default=65000)
    recargo_instalacion       = models.DecimalField(max_digits=5,  decimal_places=2, default=20)
    recargo_diseno            = models.DecimalField(max_digits=5,  decimal_places=2, default=30)
    costo_transporte_local    = models.DecimalField(max_digits=10, decimal_places=2, default=15000)
    costo_transporte_nacional = models.DecimalField(max_digits=10, decimal_places=2, default=80000)
    area_minima_m2            = models.DecimalField(max_digits=6,  decimal_places=3, default=0.25)
    actualizado_en            = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuracion de Precios'

    def __str__(self):
        return f"{self.nombre} ({'activa' if self.activo else 'inactiva'})"
