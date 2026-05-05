from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    total_facturado  = serializers.ReadOnlyField()
    total_pagado     = serializers.ReadOnlyField()
    saldo_deuda      = serializers.ReadOnlyField()
    estado_financiero= serializers.ReadOnlyField()

    class Meta:
        model  = Cliente
        fields = '__all__'
