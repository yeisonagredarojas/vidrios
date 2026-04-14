from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_configuracion, name='lista_configuracion'),
    path('editar/<int:pk>/', views.editar_configuracion, name='editar_configuracion'),
]
