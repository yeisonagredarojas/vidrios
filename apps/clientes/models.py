from django.db import models
from django.db.models import Sum


class Cliente(models.Model):
    nombre        = models.CharField(max_length=200)
    telefono      = models.CharField(max_length=20)
    correo        = models.EmailField(blank=True, null=True)
    direccion     = models.TextField(blank=True)
    ciudad        = models.CharField(max_length=100)
    notas         = models.TextField(blank=True)
    activo        = models.BooleanField(default=True)
    fecha_registro= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"

    @property
    def total_facturado(self):
        return float(self.pedidos.exclude(estado='cancelado')
                     .aggregate(t=Sum('precio_total'))['t'] or 0)

    @property
    def total_pagado(self):
        from apps.pagos.models import Pago
        return float(Pago.objects.filter(pedido__cliente=self)
                     .aggregate(t=Sum('monto'))['t'] or 0)

    @property
    def saldo_deuda(self):
        return round(self.total_facturado - self.total_pagado, 2)

    @property
    def estado_financiero(self):
        return 'paz_y_salvo' if self.saldo_deuda <= 0 else 'con_deuda'
