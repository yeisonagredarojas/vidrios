"""
Modelo de Inventario de materiales.
"""
from django.db import models


class Material(models.Model):
    UNIDAD = [
        ('m2', 'Metros cuadrados (m²)'),
        ('unidad', 'Unidades'),
        ('kg', 'Kilogramos'),
        ('litros', 'Litros'),
        ('metros', 'Metros lineales'),
        ('rollos', 'Rollos'),
    ]

    tipo_material = models.CharField(max_length=200, verbose_name="Tipo de material")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    cantidad = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Cantidad disponible")
    unidad = models.CharField(max_length=20, choices=UNIDAD, verbose_name="Unidad de medida")
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=5, verbose_name="Stock mínimo de alerta")
    proveedor = models.ForeignKey(
        'proveedores.Proveedor', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='materiales', verbose_name="Proveedor principal"
    )
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Precio de compra")
    ubicacion = models.CharField(max_length=100, blank=True, verbose_name="Ubicación en bodega")
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales / Inventario"
        ordering = ['tipo_material']

    def __str__(self):
        return f"{self.tipo_material} ({self.cantidad} {self.get_unidad_display()})"

    @property
    def bajo_stock(self):
        return self.cantidad <= self.stock_minimo

    @property
    def estado_stock(self):
        if self.cantidad == 0:
            return "agotado"
        elif self.bajo_stock:
            return "bajo"
        return "normal"
