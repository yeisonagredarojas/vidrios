"""
Modelo de Cotizaciones - reemplaza Excel de precios.
Permite parametrizar todos los precios del negocio.
"""
from django.db import models


class ConfiguracionPrecios(models.Model):
    """
    Tabla parametrizable con todos los precios del negocio.
    Solo debe existir un registro activo. Editable desde el admin.
    """
    nombre = models.CharField(max_length=100, default="Configuración Principal")
    activo = models.BooleanField(default=True)

    # Precios por m² según tipo de vidrio (en pesos colombianos)
    precio_vidrio_normal_m2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=25000,
        verbose_name="Precio vidrio normal ($/m²)"
    )
    precio_vidrio_tallado_m2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=45000,
        verbose_name="Precio vidrio tallado ($/m²)"
    )
    precio_espejo_m2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=35000,
        verbose_name="Precio espejo ($/m²)"
    )
    precio_vidrio_templado_m2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=80000,
        verbose_name="Precio vidrio templado ($/m²)"
    )
    precio_vidrio_laminado_m2 = models.DecimalField(
        max_digits=10, decimal_places=2, default=65000,
        verbose_name="Precio vidrio laminado ($/m²)"
    )

    # Recargo por tipo de trabajo
    recargo_instalacion = models.DecimalField(
        max_digits=5, decimal_places=2, default=20.00,
        verbose_name="Recargo instalación (%)"
    )
    recargo_diseno = models.DecimalField(
        max_digits=5, decimal_places=2, default=30.00,
        verbose_name="Recargo diseño/tallado (%)"
    )

    # Transporte
    costo_transporte_local = models.DecimalField(
        max_digits=10, decimal_places=2, default=15000,
        verbose_name="Costo transporte local ($)"
    )
    costo_transporte_nacional = models.DecimalField(
        max_digits=10, decimal_places=2, default=80000,
        verbose_name="Costo transporte nacional ($)"
    )

    # Área mínima cobrable
    area_minima_m2 = models.DecimalField(
        max_digits=6, decimal_places=3, default=0.25,
        verbose_name="Área mínima cobrable (m²)"
    )

    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración de Precios"
        verbose_name_plural = "Configuraciones de Precios"

    def __str__(self):
        return f"{self.nombre} ({'Activa' if self.activo else 'Inactiva'})"
