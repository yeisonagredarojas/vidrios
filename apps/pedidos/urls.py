from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pedidos, name='lista_pedidos'),
    path('nuevo/', views.crear_pedido, name='crear_pedido'),
    path('<int:pk>/', views.detalle_pedido, name='detalle_pedido'),
    path('<int:pk>/editar/', views.editar_pedido, name='editar_pedido'),
    path('calcular-precio/', views.calcular_precio_ajax, name='calcular_precio_ajax'),
]
