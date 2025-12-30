"""
Utilidades para WhatsApp y mensajería
"""
from urllib.parse import quote


def generar_mensaje_whatsapp(nombre_producto=None):
    """
    Genera el mensaje de WhatsApp optimizado para conversión.
    
    Args:
        nombre_producto (str, optional): Nombre del producto. Si es None, usa "un diseño personalizado"
    
    Returns:
        str: Mensaje URL-encoded listo para usar en wa.me
    """
    if nombre_producto:
        producto_texto = nombre_producto
    else:
        producto_texto = "un diseño personalizado"
    
    mensaje = f"""Hola! 😊
Vi este diseño en la web y me encantó.

👉 Producto: {producto_texto}

Quería saber cómo lo personalizamos 💖"""
    
    return quote(mensaje)

