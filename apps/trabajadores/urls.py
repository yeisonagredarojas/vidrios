from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_trabajadores, name='lista_trabajadores'),
    path('nuevo/', views.crear_trabajador, name='crear_trabajador'),
    path('<int:pk>/editar/', views.editar_trabajador, name='editar_trabajador'),
]
