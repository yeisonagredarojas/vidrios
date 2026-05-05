"""
Servicio central de cotización automática.
Importado por pedidos y por el endpoint público de cotización.
"""
from decimal import Decimal
from django.conf import settings


def calcular_precio(datos: dict, config) -> dict:
    tipo_vidrio       = datos.get('tipo_vidrio', 'normal')
    ancho             = Decimal(str(datos.get('ancho', 0)))
    alto              = Decimal(str(datos.get('alto', 0)))
    tipo_trabajo      = datos.get('tipo_trabajo', 'corte')
    es_envio_nacional = datos.get('es_envio_nacional', False)

    _validar_medidas(tipo_vidrio, float(ancho), float(alto))

    area          = ancho * alto
    area_cobrable = max(area, config.area_minima_m2)

    precios = {
        'normal'  : config.precio_vidrio_normal_m2,
        'tallado' : config.precio_vidrio_tallado_m2,
        'espejo'  : config.precio_espejo_m2,
        'templado': config.precio_vidrio_templado_m2,
        'laminado': config.precio_vidrio_laminado_m2,
    }
    precio_m2    = precios.get(tipo_vidrio, config.precio_vidrio_normal_m2)
    precio_vidrio= area_cobrable * precio_m2

    recargo = Decimal('0')
    if tipo_trabajo in ('instalacion', 'corte_instalacion'):
        recargo = precio_vidrio * (config.recargo_instalacion / 100)
    elif tipo_trabajo == 'diseno':
        recargo = precio_vidrio * (config.recargo_diseno / 100)

    transporte   = config.costo_transporte_nacional if es_envio_nacional else config.costo_transporte_local
    precio_total = precio_vidrio + recargo + transporte

    return {
        'area'            : float(area),
        'area_cobrable'   : float(area_cobrable),
        'precio_m2'       : float(precio_m2),
        'precio_vidrio'   : float(precio_vidrio),
        'recargo_trabajo' : float(recargo),
        'costo_transporte': float(transporte),
        'precio_total'    : float(precio_total),
    }


def _validar_medidas(tipo_vidrio, ancho, alto):
    s = settings
    if tipo_vidrio == 'normal':
        if ancho > s.VIDRIO_ESTANDAR_MAX_ANCHO:
            raise ValueError(f"Ancho {ancho}m supera el maximo ({s.VIDRIO_ESTANDAR_MAX_ANCHO}m) para vidrio normal")
        if alto > s.VIDRIO_ESTANDAR_MAX_ALTO:
            raise ValueError(f"Alto {alto}m supera el maximo ({s.VIDRIO_ESTANDAR_MAX_ALTO}m) para vidrio normal")
    elif tipo_vidrio == 'tallado':
        if ancho > s.VIDRIO_FIGURITA_MAX_ANCHO:
            raise ValueError(f"Ancho {ancho}m supera el maximo ({s.VIDRIO_FIGURITA_MAX_ANCHO}m) para vidrio tallado")
        if alto > s.VIDRIO_FIGURITA_MAX_ALTO:
            raise ValueError(f"Alto {alto}m supera el maximo ({s.VIDRIO_FIGURITA_MAX_ALTO}m) para vidrio tallado")
