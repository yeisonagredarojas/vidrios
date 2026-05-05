from rest_framework import serializers
from .models import Pedido
from apps.cotizaciones.models import ConfiguracionPrecios
from apps.cotizaciones.services import calcular_precio


class PedidoSerializer(serializers.ModelSerializer):
    total_pagado    = serializers.ReadOnlyField()
    saldo_pendiente = serializers.ReadOnlyField()
    cliente_nombre  = serializers.CharField(source='cliente.nombre', read_only=True)

    class Meta:
        model  = Pedido
        fields = '__all__'
        read_only_fields = ['area_calculada', 'precio_total', 'fecha']

    def validate(self, data):
        """Calcula precio automatico al crear/actualizar."""
        config = ConfiguracionPrecios.objects.filter(activo=True).first()
        if not config:
            raise serializers.ValidationError("No hay configuracion de precios activa.")
        try:
            resultado = calcular_precio({
                'tipo_vidrio'      : data.get('tipo_vidrio', ''),
                'ancho'            : float(data.get('ancho', 0)),
                'alto'             : float(data.get('alto', 0)),
                'tipo_trabajo'     : data.get('tipo_trabajo', 'corte'),
                'es_envio_nacional': data.get('es_envio_nacional', False),
            }, config)
            data['precio_total'] = resultado['precio_total']
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return data
