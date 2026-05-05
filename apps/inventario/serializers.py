from rest_framework import serializers
from .models import Material


class MaterialSerializer(serializers.ModelSerializer):
    bajo_stock   = serializers.ReadOnlyField()
    estado_stock = serializers.ReadOnlyField()

    class Meta:
        model  = Material
        fields = '__all__'
