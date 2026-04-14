"""
Modelo de Clientes - reemplaza el Excel de clientes.
"""
from django.db import models
from django.db.models import Sum


class Cliente(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre completo")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono / WhatsApp")
    correo = models.EmailField(blank=True, null=True, verbose_name="Correo electrónico")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    notas = models.TextField(blank=True, verbose_name="Notas adicionales")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    activo = models.BooleanField(default=True, verbose_name="Cliente activo")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"

    @property
    def total_pedidos(self):
        return self.pedidos.aggregate(total=Sum('precio_total'))['total'] or 0

    @property
    def total_pagado(self):
        from apps.pagos.models import Pago
        return Pago.objects.filter(pedido__cliente=self).aggregate(total=Sum('monto'))['total'] or 0

    @property
    def saldo_deuda(self):
        return self.total_pedidos - self.total_pagado

    @property
    def esta_al_dia(self):
        return self.saldo_deuda <= 0

    @property
    def estado_financiero(self):
        deuda = self.saldo_deuda
        if deuda <= 0:
            return "paz_y_salvo"
        elif deuda < 100000:
            return "deuda_menor"
        return "deuda_mayor"
