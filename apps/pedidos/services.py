"""
Servicios de notificación para pedidos.
Integración con WhatsApp Business API y correo electrónico.
"""
import requests
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def enviar_whatsapp_notificacion(telefono: str, mensaje: str) -> bool:
    """
    Envía mensaje de WhatsApp usando la API de WhatsApp Business.
    Si no hay token configurado, simula el envío (modo desarrollo).
    """
    token = settings.WHATSAPP_API_TOKEN
    phone_id = settings.WHATSAPP_PHONE_ID

    if not token or not phone_id:
        # Modo simulación - solo loguea
        logger.info(f"[WhatsApp MOCK] → {telefono}: {mensaje}")
        return True

    try:
        url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": telefono.replace('+', '').replace(' ', ''),
            "type": "text",
            "text": {"body": mensaje}
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        logger.info(f"WhatsApp enviado a {telefono}")
        return True
    except Exception as e:
        logger.error(f"Error enviando WhatsApp a {telefono}: {e}")
        return False


def notificar_pedido_creado(pedido) -> None:
    """Notifica al cliente cuando se crea un pedido."""
    mensaje = (
        f"✅ *{settings.EMPRESA_NOMBRE}*\n\n"
        f"Hola {pedido.cliente.nombre}, tu pedido #{pedido.pk} ha sido registrado.\n\n"
        f"📋 Detalles:\n"
        f"• Vidrio: {pedido.get_tipo_vidrio_display()}\n"
        f"• Medidas: {pedido.ancho}m × {pedido.alto}m\n"
        f"• Trabajo: {pedido.get_tipo_trabajo_display()}\n"
        f"• Total: ${pedido.precio_total:,.0f}\n\n"
        f"Estado: {pedido.get_estado_display()}\n"
        f"Gracias por confiar en nosotros. 🏭"
    )
    enviar_whatsapp_notificacion(pedido.cliente.telefono, mensaje)

    # Email si tiene correo
    if pedido.cliente.correo:
        _enviar_email_pedido(pedido)


def notificar_cambio_estado(pedido) -> None:
    """Notifica al cliente cuando cambia el estado de su pedido."""
    emojis = {
        'cotizado': '📝', 'abonado': '💰',
        'en_proceso': '🔧', 'terminado': '✅', 'cancelado': '❌'
    }
    emoji = emojis.get(pedido.estado, '📋')
    mensaje = (
        f"{emoji} *{settings.EMPRESA_NOMBRE}*\n\n"
        f"Hola {pedido.cliente.nombre}!\n"
        f"Tu pedido #{pedido.pk} cambió de estado:\n\n"
        f"Estado actual: *{pedido.get_estado_display()}*\n\n"
        f"Para más info: {settings.EMPRESA_TELEFONO}"
    )
    enviar_whatsapp_notificacion(pedido.cliente.telefono, mensaje)


def _enviar_email_pedido(pedido) -> None:
    """Envía confirmación de pedido por correo."""
    try:
        send_mail(
            subject=f"Pedido #{pedido.pk} registrado - {settings.EMPRESA_NOMBRE}",
            message=(
                f"Hola {pedido.cliente.nombre},\n\n"
                f"Tu pedido #{pedido.pk} ha sido registrado.\n"
                f"Total: ${pedido.precio_total:,.0f}\n\n"
                f"Gracias por confiar en {settings.EMPRESA_NOMBRE}."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[pedido.cliente.correo],
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Error enviando email: {e}")
