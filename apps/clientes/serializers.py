from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    saldo_deuda = serializers.ReadOnlyField()
    esta_al_dia = serializers.ReadOnlyField()
    total_pedidos_count = serializers.SerializerMethodField()

    class Meta:
        model = Cliente
        fields = '__all__'

    def get_total_pedidos_count(self, obj):
        return obj.pedidos.count()
