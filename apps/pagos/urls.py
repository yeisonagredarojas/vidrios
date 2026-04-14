from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pagos, name='lista_pagos'),
    path('nuevo/', views.registrar_pago, name='registrar_pago'),
    path('deudas/', views.deudas, name='deudas'),
]
