from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Pago
from .serializers import PagoSerializer
from apps.clientes.models import Cliente
from apps.clientes.serializers import ClienteSerializer


class PagoViewSet(viewsets.ModelViewSet):
    queryset         = Pago.objects.select_related('cliente', 'pedido')
    serializer_class = PagoSerializer

    @action(detail=False, methods=['get'], url_path='deudas')
    def deudas(self, request):
        """GET /api/pagos/deudas/ — lista clientes con saldo pendiente."""
        resultado = []
        for cliente in Cliente.objects.filter(activo=True):
            if cliente.saldo_deuda > 0:
                resultado.append({
                    'id'           : cliente.id,
                    'nombre'       : cliente.nombre,
                    'telefono'     : cliente.telefono,
                    'ciudad'       : cliente.ciudad,
                    'total_facturado': cliente.total_facturado,
                    'total_pagado' : cliente.total_pagado,
                    'saldo_deuda'  : cliente.saldo_deuda,
                })
        resultado.sort(key=lambda x: x['saldo_deuda'], reverse=True)
        return Response(resultado)
