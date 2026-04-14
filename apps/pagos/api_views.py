from rest_framework import viewsets
from .models import Pago
from .serializers import PagoSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.select_related('cliente', 'pedido').all()
    serializer_class = PagoSerializer
