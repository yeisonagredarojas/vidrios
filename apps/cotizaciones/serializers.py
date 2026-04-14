from rest_framework import serializers
from .models import ConfiguracionPrecios

class ConfiguracionPreciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionPrecios
        fields = '__all__'
