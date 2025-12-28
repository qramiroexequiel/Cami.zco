from django.conf import settings


def whatsapp_number(request):
    """Context processor para el número de WhatsApp"""
    return {
        'whatsapp_number': getattr(settings, 'WHATSAPP_NUMBER', '5491112345678')
    }


def google_analytics(request):
    """Context processor para Google Analytics 4"""
    ga4_id = getattr(settings, 'GA4_MEASUREMENT_ID', '')
    return {
        'ga4_id': ga4_id if ga4_id else None
    }

