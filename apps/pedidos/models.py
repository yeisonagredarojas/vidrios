"""
Modelo de Pedidos - núcleo del sistema ERP.
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Pedido(models.Model):
    TIPO_VIDRIO = [
        ('normal', 'Vidrio Normal'),
        ('tallado', 'Vidrio Tallado / Figuritas'),
        ('espejo', 'Espejo'),
        ('templado', 'Vidrio Templado'),
        ('laminado', 'Vidrio Laminado'),
    ]
    TIPO_TRABAJO = [
        ('corte', 'Corte'),
        ('instalacion', 'Instalación'),
        ('diseno', 'Diseño / Tallado'),
        ('corte_instalacion', 'Corte + Instalación'),
    ]
    ESTADO = [
        ('cotizado', 'Cotizado'),
        ('abonado', 'Abonado'),
        ('en_proceso', 'En Proceso'),
        ('terminado', 'Terminado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        'clientes.Cliente', on_delete=models.PROTECT,
        related_name='pedidos', verbose_name="Cliente"
    )
    tipo_vidrio = models.CharField(max_length=20, choices=TIPO_VIDRIO, verbose_name="Tipo de vidrio")
    ancho = models.DecimalField(max_digits=6, decimal_places=3, verbose_name="Ancho (metros)")
    alto = models.DecimalField(max_digits=6, decimal_places=3, verbose_name="Alto (metros)")
    area_calculada = models.DecimalField(
        max_digits=8, decimal_places=4, editable=False,
        verbose_name="Área calculada (m²)"
    )
    tipo_trabajo = models.CharField(max_length=30, choices=TIPO_TRABAJO, verbose_name="Tipo de trabajo")
    descripcion = models.TextField(blank=True, verbose_name="Descripción / Diseño")
    imagen = models.ImageField(upload_to='pedidos/', blank=True, null=True, verbose_name="Imagen de referencia")
    direccion_entrega = models.TextField(blank=True, verbose_name="Dirección de entrega")
    ciudad_entrega = models.CharField(max_length=100, blank=True, verbose_name="Ciudad de entrega")
    es_envio_nacional = models.BooleanField(default=False, verbose_name="¿Envío nacional?")
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio total")
    estado = models.CharField(max_length=20, choices=ESTADO, default='cotizado', verbose_name="Estado")
    trabajador_asignado = models.ForeignKey(
        'trabajadores.Trabajador', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='pedidos', verbose_name="Trabajador asignado"
    )
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de pedido")
    fecha_entrega_estimada = models.DateField(null=True, blank=True, verbose_name="Fecha estimada de entrega")
    notas_internas = models.TextField(blank=True, verbose_name="Notas internas")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha']

    def __str__(self):
        return f"Pedido #{self.pk} - {self.cliente.nombre} ({self.get_estado_display()})"

    def clean(self):
        """Valida las medidas máximas según tipo de vidrio."""
        ancho = float(self.ancho or 0)
        alto = float(self.alto or 0)

        if self.tipo_vidrio == 'normal':
            if ancho > settings.VIDRIO_ESTANDAR_MAX_ANCHO:
                raise ValidationError(
                    f"El ancho máximo para vidrio normal es {settings.VIDRIO_ESTANDAR_MAX_ANCHO}m"
                )
            if alto > settings.VIDRIO_ESTANDAR_MAX_ALTO:
                raise ValidationError(
                    f"El alto máximo para vidrio normal es {settings.VIDRIO_ESTANDAR_MAX_ALTO}m"
                )
        elif self.tipo_vidrio in ('tallado',):
            if ancho > settings.VIDRIO_FIGURITA_MAX_ANCHO:
                raise ValidationError(
                    f"El ancho máximo para vidrio tallado es {settings.VIDRIO_FIGURITA_MAX_ANCHO}m"
                )
            if alto > settings.VIDRIO_FIGURITA_MAX_ALTO:
                raise ValidationError(
                    f"El alto máximo para vidrio tallado es {settings.VIDRIO_FIGURITA_MAX_ALTO}m"
                )

    def save(self, *args, **kwargs):
        self.area_calculada = self.ancho * self.alto
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_pagado(self):
        return self.pagos.aggregate(
            total=__import__('django.db.models', fromlist=['Sum']).Sum('monto')
        )['total'] or 0

    @property
    def saldo_pendiente(self):
        from django.db.models import Sum
        pagado = self.pagos.aggregate(total=Sum('monto'))['total'] or 0
        return float(self.precio_total) - float(pagado)
