from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'ciudad', 'fecha_registro', 'activo']
    list_filter = ['ciudad', 'activo']
    search_fields = ['nombre', 'telefono', 'correo']
