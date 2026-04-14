"""
Context processors: inyectan variables globales en todos los templates.
"""
from django.conf import settings


def empresa_info(request):
    """Expone información de la empresa a todos los templates."""
    return {
        'EMPRESA_NOMBRE': settings.EMPRESA_NOMBRE,
        'EMPRESA_TELEFONO': settings.EMPRESA_TELEFONO,
        'EMPRESA_CIUDAD': settings.EMPRESA_CIUDAD,
    }
