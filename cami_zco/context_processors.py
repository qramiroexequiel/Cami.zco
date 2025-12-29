from django.conf import settings


def whatsapp_number(request):
    """Context processor para el número de WhatsApp"""
    # Manejo seguro para serverless: nunca fallar, siempre retornar un valor
    try:
        whatsapp = getattr(settings, 'WHATSAPP_NUMBER', '5491112345678')
        # Validar que sea un string no vacío
        if not whatsapp or not isinstance(whatsapp, str):
            whatsapp = '5491112345678'
    except (AttributeError, Exception):
        # Si hay cualquier error, usar default seguro
        whatsapp = '5491112345678'
    
    return {
        'whatsapp_number': whatsapp
    }


def google_analytics(request):
    """Context processor para Google Analytics 4"""
    # Manejo seguro para serverless: nunca fallar, siempre retornar un valor
    try:
        ga4_id = getattr(settings, 'GA4_MEASUREMENT_ID', '')
        # Validar que sea un string válido o None
        if ga4_id and isinstance(ga4_id, str) and ga4_id.strip():
            ga4_id = ga4_id.strip()
        else:
            ga4_id = None
    except (AttributeError, Exception):
        # Si hay cualquier error, retornar None (no crítico)
        ga4_id = None
    
    return {
        'ga4_id': ga4_id
    }

