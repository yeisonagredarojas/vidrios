"""
URLs para la API REST del sistema.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.clientes.api_views import ClienteViewSet
from apps.pedidos.api_views import PedidoViewSet
from apps.pagos.api_views import PagoViewSet
from apps.cotizaciones.api_views import CotizacionViewSet, calcular_cotizacion
from apps.inventario.api_views import MaterialViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='api-clientes')
router.register(r'pedidos', PedidoViewSet, basename='api-pedidos')
router.register(r'pagos', PagoViewSet, basename='api-pagos')
router.register(r'cotizaciones', CotizacionViewSet, basename='api-cotizaciones')
router.register(r'inventario', MaterialViewSet, basename='api-inventario')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('cotizaciones/calcular/', calcular_cotizacion, name='api-calcular-cotizacion'),
]
