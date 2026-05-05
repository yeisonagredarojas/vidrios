from django.db import models


class Material(models.Model):
    UNIDAD = [
        ('m2','Metros cuadrados'),('unidad','Unidades'),
        ('kg','Kilogramos'),('litros','Litros'),('metros','Metros lineales'),
    ]
    tipo_material = models.CharField(max_length=200)
    descripcion   = models.TextField(blank=True)
    cantidad      = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    unidad        = models.CharField(max_length=20, choices=UNIDAD)
    stock_minimo  = models.DecimalField(max_digits=10, decimal_places=3, default=5)
    proveedor     = models.ForeignKey('proveedores.Proveedor', on_delete=models.SET_NULL, null=True, blank=True)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ubicacion     = models.CharField(max_length=100, blank=True)
    activo        = models.BooleanField(default=True)
    actualizado_en= models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tipo_material']

    def __str__(self):
        return f"{self.tipo_material} — {self.cantidad} {self.unidad}"

    @property
    def bajo_stock(self):
        return self.cantidad <= self.stock_minimo

    @property
    def estado_stock(self):
        if self.cantidad == 0:   return 'agotado'
        if self.bajo_stock:      return 'bajo'
        return 'normal'
