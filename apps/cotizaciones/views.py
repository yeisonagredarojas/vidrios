from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import ConfiguracionPrecios
from .serializers import ConfiguracionPreciosSerializer, CotizarInputSerializer
from .services import calcular_precio


class ConfiguracionPreciosViewSet(viewsets.ModelViewSet):
    queryset         = ConfiguracionPrecios.objects.all()
    serializer_class = ConfiguracionPreciosSerializer


@api_view(['POST'])
@permission_classes([AllowAny])  # publico — cualquiera puede cotizar
def cotizar(request):
    """
    Calcula el precio de un vidrio sin autenticacion.
    Body JSON:
        {"tipo_vidrio":"normal","ancho":1.5,"alto":2.0,
         "tipo_trabajo":"instalacion","es_envio_nacional":false}
    """
    ser = CotizarInputSerializer(data=request.data)
    if not ser.is_valid():
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    config = ConfiguracionPrecios.objects.filter(activo=True).first()
    if not config:
        return Response({'error': 'No hay configuracion de precios activa'}, status=500)

    try:
        resultado = calcular_precio(ser.validated_data, config)
        return Response(resultado)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
