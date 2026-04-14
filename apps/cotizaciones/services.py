"""
Servicio de cotización automática.
Calcula precios según tipo de vidrio, medidas y tipo de trabajo.
"""
from decimal import Decimal


def calcular_precio(datos: dict, config) -> dict:
    """
    Calcula el precio de un pedido automáticamente.

    Args:
        datos: dict con keys: tipo_vidrio, ancho, alto, tipo_trabajo,
                               es_envio_nacional
        config: instancia de ConfiguracionPrecios

    Returns:
        dict con precio_total, area, precio_m2, desglose
    """
    from django.conf import settings

    tipo_vidrio = datos.get('tipo_vidrio', 'normal')
    ancho = Decimal(str(datos.get('ancho', 0)))
    alto = Decimal(str(datos.get('alto', 0)))
    tipo_trabajo = datos.get('tipo_trabajo', 'corte')
    es_envio_nacional = datos.get('es_envio_nacional', False)

    # Validar medidas
    _validar_medidas(tipo_vidrio, float(ancho), float(alto), settings)

    # Calcular área (mínimo configurable)
    area = ancho * alto
    area_cobrable = max(area, config.area_minima_m2)

    # Precio base por m² según tipo de vidrio
    precios_m2 = {
        'normal': config.precio_vidrio_normal_m2,
        'tallado': config.precio_vidrio_tallado_m2,
        'espejo': config.precio_espejo_m2,
        'templado': config.precio_vidrio_templado_m2,
        'laminado': config.precio_vidrio_laminado_m2,
    }
    precio_m2 = precios_m2.get(tipo_vidrio, config.precio_vidrio_normal_m2)
    precio_vidrio = area_cobrable * precio_m2

    # Recargo por tipo de trabajo
    recargo = Decimal('0')
    if tipo_trabajo == 'instalacion':
        recargo = precio_vidrio * (config.recargo_instalacion / 100)
    elif tipo_trabajo == 'diseno':
        recargo = precio_vidrio * (config.recargo_diseno / 100)
    elif tipo_trabajo == 'corte_instalacion':
        recargo = precio_vidrio * (config.recargo_instalacion / 100)

    # Transporte
    if es_envio_nacional:
        costo_transporte = config.costo_transporte_nacional
    else:
        costo_transporte = config.costo_transporte_local

    precio_total = precio_vidrio + recargo + costo_transporte

    return {
        'area': float(area),
        'area_cobrable': float(area_cobrable),
        'precio_m2': float(precio_m2),
        'precio_vidrio': float(precio_vidrio),
        'recargo_trabajo': float(recargo),
        'costo_transporte': float(costo_transporte),
        'precio_total': float(precio_total),
        'desglose': {
            'Vidrio ({:.4f} m² × ${:,.0f}/m²)'.format(float(area_cobrable), float(precio_m2)): float(precio_vidrio),
            'Mano de obra ({})'.format(tipo_trabajo): float(recargo),
            'Transporte': float(costo_transporte),
        }
    }


def _validar_medidas(tipo_vidrio: str, ancho: float, alto: float, settings) -> None:
    """Lanza ValueError si las medidas superan los límites del tipo de vidrio."""
    if tipo_vidrio == 'normal':
        if ancho > settings.VIDRIO_ESTANDAR_MAX_ANCHO:
            raise ValueError(
                f"Ancho {ancho}m supera el máximo de {settings.VIDRIO_ESTANDAR_MAX_ANCHO}m para vidrio normal"
            )
        if alto > settings.VIDRIO_ESTANDAR_MAX_ALTO:
            raise ValueError(
                f"Alto {alto}m supera el máximo de {settings.VIDRIO_ESTANDAR_MAX_ALTO}m para vidrio normal"
            )
    elif tipo_vidrio == 'tallado':
        if ancho > settings.VIDRIO_FIGURITA_MAX_ANCHO:
            raise ValueError(
                f"Ancho {ancho}m supera el máximo de {settings.VIDRIO_FIGURITA_MAX_ANCHO}m para vidrio tallado"
            )
        if alto > settings.VIDRIO_FIGURITA_MAX_ALTO:
            raise ValueError(
                f"Alto {alto}m supera el máximo de {settings.VIDRIO_FIGURITA_MAX_ALTO}m para vidrio tallado"
            )
