from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_inventario, name='lista_inventario'),
    path('nuevo/', views.crear_material, name='crear_material'),
    path('<int:pk>/editar/', views.editar_material, name='editar_material'),
]
