from django.conf import settings


def whatsapp_number(request):
    """Context processor para el número de WhatsApp"""
    try:
        whatsapp = getattr(settings, 'WHATSAPP_NUMBER', '5491112345678')
        if not whatsapp or not isinstance(whatsapp, str):
            whatsapp = '5491112345678'
    except (AttributeError, Exception):
        whatsapp = '5491112345678'
    
    return {
        'whatsapp_number': whatsapp
    }


def google_analytics(request):
    """Context processor para Google Analytics 4"""
    try:
        ga4_id = getattr(settings, 'GA4_MEASUREMENT_ID', '')
        if ga4_id and isinstance(ga4_id, str) and ga4_id.strip():
            ga4_id = ga4_id.strip()
        else:
            ga4_id = None
    except (AttributeError, Exception):
        ga4_id = None
    
    return {
        'ga4_id': ga4_id
    }


def configuracion_sitio(request):
    """Context processor para ConfiguracionSitio"""
    try:
        from catalogo.models import ConfiguracionSitio
        config = ConfiguracionSitio.get_config()
    except Exception:
        config = None
    
    return {
        'config_sitio': config
    }

