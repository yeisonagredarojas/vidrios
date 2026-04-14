from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pedido
from .serializers import PedidoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.select_related('cliente').all()
    serializer_class = PedidoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['estado', 'tipo_vidrio', 'cliente']
    search_fields = ['cliente__nombre']
