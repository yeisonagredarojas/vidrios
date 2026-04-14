from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'cliente', 'tipo_vidrio', 'area_calculada', 'precio_total', 'estado', 'fecha']
    list_filter = ['estado', 'tipo_vidrio']
    search_fields = ['cliente__nombre']
