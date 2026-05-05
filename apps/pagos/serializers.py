from rest_framework import serializers
from .models import Pago


class PagoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    pedido_estado  = serializers.CharField(source='pedido.estado', read_only=True)

    class Meta:
        model  = Pago
        fields = '__all__'
