from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Pedido
from .serializers import PedidoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset         = Pedido.objects.select_related('cliente', 'trabajador_asignado')
    serializer_class = PedidoSerializer
    filter_backends  = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['estado', 'tipo_vidrio', 'cliente', 'es_envio_nacional']
    search_fields    = ['cliente__nombre', 'descripcion']
