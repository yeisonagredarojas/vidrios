from rest_framework import serializers
from .models import ConfiguracionPrecios


class ConfiguracionPreciosSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ConfiguracionPrecios
        fields = '__all__'


class CotizarInputSerializer(serializers.Serializer):
    tipo_vidrio       = serializers.ChoiceField(choices=['normal','tallado','espejo','templado','laminado'])
    ancho             = serializers.FloatField(min_value=0.01)
    alto              = serializers.FloatField(min_value=0.01)
    tipo_trabajo      = serializers.ChoiceField(choices=['corte','instalacion','diseno','corte_instalacion'], default='corte')
    es_envio_nacional = serializers.BooleanField(default=False)
