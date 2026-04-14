"""
URLs principales del proyecto ERP Vidrios.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard principal
    path('', views.home_redirect, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Módulos del sistema
    path('clientes/', include('apps.clientes.urls')),
    path('pedidos/', include('apps.pedidos.urls')),
    path('pagos/', include('apps.pagos.urls')),
    path('inventario/', include('apps.inventario.urls')),
    path('cotizaciones/', include('apps.cotizaciones.urls')),
    path('trabajadores/', include('apps.trabajadores.urls')),
    path('proveedores/', include('apps.proveedores.urls')),

    # Sitio público
    path('inicio/', views.landing_page, name='landing'),
    path('solicitar-cotizacion/', views.solicitar_cotizacion_publica, name='cotizacion_publica'),

    # API REST
    path('api/', include('core.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
