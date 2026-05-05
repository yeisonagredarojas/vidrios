from django.db import models


class Pago(models.Model):
    TIPO_PAGO = [
        ('efectivo','Efectivo'),('transferencia','Transferencia'),
        ('nequi','Nequi'),('daviplata','Daviplata'),('otro','Otro'),
    ]
    cliente      = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, related_name='pagos')
    pedido       = models.ForeignKey('pedidos.Pedido', on_delete=models.PROTECT, related_name='pagos')
    monto        = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_pago   = models.DateField()
    tipo_pago    = models.CharField(max_length=20, choices=TIPO_PAGO, default='efectivo')
    referencia   = models.CharField(max_length=100, blank=True)
    notas        = models.TextField(blank=True)
    creado_en    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"Pago ${self.monto} — {self.cliente.nombre} ({self.fecha_pago})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._actualizar_estado_pedido()

    def _actualizar_estado_pedido(self):
        from django.db.models import Sum
        pedido = self.pedido
        pagado = pedido.pagos.aggregate(t=Sum('monto'))['t'] or 0
        if float(pagado) >= float(pedido.precio_total):
            if pedido.estado not in ('terminado','cancelado'):
                type(pedido).objects.filter(pk=pedido.pk).update(estado='en_proceso')
        elif float(pagado) > 0 and pedido.estado == 'cotizado':
            type(pedido).objects.filter(pk=pedido.pk).update(estado='abonado')
