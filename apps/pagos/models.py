"""
Modelo de Pagos y control de deudas.
"""
from django.db import models


class Pago(models.Model):
    TIPO_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
        ('nequi', 'Nequi'),
        ('daviplata', 'Daviplata'),
        ('cheque', 'Cheque'),
        ('otro', 'Otro'),
    ]

    cliente = models.ForeignKey(
        'clientes.Cliente', on_delete=models.PROTECT,
        related_name='pagos', verbose_name="Cliente"
    )
    pedido = models.ForeignKey(
        'pedidos.Pedido', on_delete=models.PROTECT,
        related_name='pagos', verbose_name="Pedido"
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto pagado")
    fecha_pago = models.DateField(verbose_name="Fecha de pago")
    tipo_pago = models.CharField(max_length=20, choices=TIPO_PAGO, default='efectivo', verbose_name="Tipo de pago")
    referencia = models.CharField(max_length=100, blank=True, verbose_name="Referencia / Comprobante")
    notas = models.TextField(blank=True, verbose_name="Notas")
    registrado_por = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True,
        verbose_name="Registrado por"
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"Pago ${self.monto:,.0f} - {self.cliente.nombre} ({self.fecha_pago})"

    def save(self, *args, **kwargs):
        # Actualizar estado del pedido según pagos
        super().save(*args, **kwargs)
        self._actualizar_estado_pedido()

    def _actualizar_estado_pedido(self):
        """Actualiza el estado del pedido según el total pagado."""
        pedido = self.pedido
        from django.db.models import Sum
        total_pagado = pedido.pagos.aggregate(total=Sum('monto'))['total'] or 0

        if float(total_pagado) >= float(pedido.precio_total):
            if pedido.estado not in ('terminado', 'cancelado'):
                pedido.estado = 'en_proceso'
        elif float(total_pagado) > 0:
            if pedido.estado == 'cotizado':
                pedido.estado = 'abonado'

        Pedido = pedido.__class__
        Pedido.objects.filter(pk=pedido.pk).update(estado=pedido.estado)
