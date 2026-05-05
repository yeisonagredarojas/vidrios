from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Sum


class Pedido(models.Model):
    TIPO_VIDRIO = [
        ('normal','Vidrio Normal'),('tallado','Vidrio Tallado'),
        ('espejo','Espejo'),('templado','Templado'),('laminado','Laminado'),
    ]
    TIPO_TRABAJO = [
        ('corte','Corte'),('instalacion','Instalacion'),
        ('diseno','Diseno'),('corte_instalacion','Corte + Instalacion'),
    ]
    ESTADO = [
        ('cotizado','Cotizado'),('abonado','Abonado'),
        ('en_proceso','En Proceso'),('terminado','Terminado'),('cancelado','Cancelado'),
    ]

    cliente              = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, related_name='pedidos')
    tipo_vidrio          = models.CharField(max_length=20, choices=TIPO_VIDRIO)
    ancho                = models.DecimalField(max_digits=6, decimal_places=3)
    alto                 = models.DecimalField(max_digits=6, decimal_places=3)
    area_calculada       = models.DecimalField(max_digits=8, decimal_places=4, editable=False, default=0)
    tipo_trabajo         = models.CharField(max_length=30, choices=TIPO_TRABAJO)
    descripcion          = models.TextField(blank=True)
    ciudad_entrega       = models.CharField(max_length=100, blank=True)
    es_envio_nacional    = models.BooleanField(default=False)
    precio_total         = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado               = models.CharField(max_length=20, choices=ESTADO, default='cotizado')
    trabajador_asignado  = models.ForeignKey(
        'trabajadores.Trabajador', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='pedidos')
    fecha                = models.DateTimeField(auto_now_add=True)
    fecha_entrega        = models.DateField(null=True, blank=True)
    notas                = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Pedido #{self.pk} — {self.cliente.nombre}"

    def clean(self):
        ancho = float(self.ancho or 0)
        alto  = float(self.alto or 0)
        s = settings
        if self.tipo_vidrio == 'normal':
            if ancho > s.VIDRIO_ESTANDAR_MAX_ANCHO:
                raise ValidationError(f"Ancho maximo vidrio normal: {s.VIDRIO_ESTANDAR_MAX_ANCHO}m")
            if alto > s.VIDRIO_ESTANDAR_MAX_ALTO:
                raise ValidationError(f"Alto maximo vidrio normal: {s.VIDRIO_ESTANDAR_MAX_ALTO}m")
        elif self.tipo_vidrio == 'tallado':
            if ancho > s.VIDRIO_FIGURITA_MAX_ANCHO:
                raise ValidationError(f"Ancho maximo vidrio tallado: {s.VIDRIO_FIGURITA_MAX_ANCHO}m")
            if alto > s.VIDRIO_FIGURITA_MAX_ALTO:
                raise ValidationError(f"Alto maximo vidrio tallado: {s.VIDRIO_FIGURITA_MAX_ALTO}m")

    def save(self, *args, **kwargs):
        self.area_calculada = self.ancho * self.alto
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_pagado(self):
        return float(self.pagos.aggregate(t=Sum('monto'))['t'] or 0)

    @property
    def saldo_pendiente(self):
        return round(float(self.precio_total) - self.total_pagado, 2)
