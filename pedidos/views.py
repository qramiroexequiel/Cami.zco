from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from django import forms
from .forms import PedidoForm
from .models import ConfiguracionPedido
from catalogo.models import Producto


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def crear_pedido(request, producto_slug=None):
    """Vista para crear un nuevo pedido"""
    producto = None
    if producto_slug:
        producto = get_object_or_404(Producto, slug=producto_slug, activo=True)

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect('pedidos:confirmacion', pedido_id=pedido.id)
    else:
        initial = {}
        if producto:
            initial['producto'] = producto.id
            # Cambiar widget a hidden cuando hay producto preseleccionado
            form = PedidoForm(initial=initial)
            form.fields['producto'].widget = forms.HiddenInput()
        else:
            form = PedidoForm(initial=initial)

    # Obtener configuración
    config = ConfiguracionPedido.objects.filter(activo=True).first()
    
    context = {
        'form': form,
        'producto': producto,
        'config': config,
    }
    return render(request, 'pedidos/formulario.html', context)


def confirmacion_pedido(request, pedido_id):
    """Vista de confirmación después de crear un pedido"""
    from .models import Pedido
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Obtener configuración
    config = ConfiguracionPedido.objects.filter(activo=True).first()
    
    # Generar link de WhatsApp
    whatsapp_destino = config.whatsapp_destino if config else '5491112345678'
    mensaje = pedido.get_mensaje_whatsapp()
    whatsapp_url = f"https://wa.me/{whatsapp_destino}?text={mensaje}"
    
    context = {
        'pedido': pedido,
        'config': config,
        'whatsapp_url': whatsapp_url,
    }
    return render(request, 'pedidos/confirmacion.html', context)
