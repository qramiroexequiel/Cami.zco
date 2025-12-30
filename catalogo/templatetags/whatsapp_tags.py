"""
Template tags para generar mensajes de WhatsApp optimizados
"""
from django import template
from catalogo.utils import generar_mensaje_whatsapp

register = template.Library()


@register.simple_tag
def mensaje_whatsapp(nombre_producto=None):
    """Genera el mensaje de WhatsApp URL-encoded."""
    return generar_mensaje_whatsapp(nombre_producto)

