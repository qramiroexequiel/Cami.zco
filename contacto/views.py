from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from .forms import ConsultaForm


@ratelimit(key='ip', rate='3/m', method='POST', block=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def crear_consulta(request):
    """Vista para crear una nueva consulta"""
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save()
            messages.success(
                request,
                f'¡Gracias {consulta.nombre}! Tu consulta fue enviada. Te responderemos por WhatsApp pronto.'
            )
            return redirect('contacto:confirmacion')
    else:
        form = ConsultaForm()

    return render(request, 'contacto/formulario.html', {'form': form})


def confirmacion_consulta(request):
    """Vista de confirmación después de enviar una consulta"""
    return render(request, 'contacto/confirmacion.html')
