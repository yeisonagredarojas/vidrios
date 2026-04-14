from django.contrib import admin
from .models import ConfiguracionPrecios

@admin.register(ConfiguracionPrecios)
class ConfiguracionPreciosAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'precio_vidrio_normal_m2', 'actualizado_en']
