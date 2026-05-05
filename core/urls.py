"""
URLs principales — solo API REST + admin.
Probar todo desde Postman.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # ── Auth JWT ──
    # POST /api/auth/token/       → obtener access + refresh token
    # POST /api/auth/token/refresh/ → renovar access token
    path('api/auth/token/',         TokenObtainPairView.as_view(),  name='token_obtain'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(),     name='token_refresh'),

    # ── Módulos ──
    path('api/clientes/',     include('apps.clientes.urls')),
    path('api/pedidos/',      include('apps.pedidos.urls')),
    path('api/pagos/',        include('apps.pagos.urls')),
    path('api/inventario/',   include('apps.inventario.urls')),
    path('api/cotizaciones/', include('apps.cotizaciones.urls')),
    path('api/trabajadores/', include('apps.trabajadores.urls')),
    path('api/proveedores/',  include('apps.proveedores.urls')),
]
