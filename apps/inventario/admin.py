from django.contrib import admin
from .models import Material

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['tipo_material', 'cantidad', 'unidad', 'stock_minimo', 'bajo_stock']
    list_filter = ['unidad']
