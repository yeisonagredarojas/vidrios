from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import ConfiguracionPrecios
from .serializers import ConfiguracionPreciosSerializer
from .services import calcular_precio

class CotizacionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ConfiguracionPrecios.objects.filter(activo=True)
    serializer_class = ConfiguracionPreciosSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def calcular_cotizacion(request):
    """Endpoint público para calcular precio de cotización."""
    config = ConfiguracionPrecios.objects.filter(activo=True).first()
    if not config:
        return Response({'error': 'Sin configuración de precios'}, status=400)
    try:
        resultado = calcular_precio(request.data, config)
        return Response({'success': True, **resultado})
    except ValueError as e:
        return Response({'success': False, 'error': str(e)}, status=400)
