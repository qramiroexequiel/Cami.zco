from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from catalogo.models import Producto, ImagenProducto, ConfiguracionSitio
from pedidos.models import Pedido, ConfiguracionPedido, ESTADO_CHOICES


@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    # Estadísticas
    pedidos_nuevos = Pedido.objects.filter(estado='nuevo').count()
    pedidos_semana = Pedido.objects.filter(
        fecha_creacion__gte=timezone.now() - timedelta(days=7)
    ).count()
    productos_activos = Producto.objects.filter(activo=True).count()
    
    # Pedidos recientes
    pedidos_recientes = Pedido.objects.all()[:5]
    
    context = {
        'pedidos_nuevos': pedidos_nuevos,
        'pedidos_semana': pedidos_semana,
        'productos_activos': productos_activos,
        'pedidos_recientes': pedidos_recientes,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def productos_lista(request):
    """Lista de productos"""
    productos = Producto.objects.all().order_by('-fecha_creacion')
    context = {
        'productos': productos,
    }
    return render(request, 'dashboard/productos_lista.html', context)


@login_required
def producto_crear(request):
    """Crear nuevo producto"""
    if request.method == 'POST':
        try:
            producto = Producto.objects.create(
                titulo=request.POST.get('titulo'),
                descripcion=request.POST.get('descripcion'),
                precio=request.POST.get('precio') or None,
                precio_desde=request.POST.get('precio_desde') == 'on',
                tiempo_estimado=request.POST.get('tiempo_estimado', '7-10 días'),
                activo=request.POST.get('activo') == 'on',
                destacado=request.POST.get('destacado') == 'on',
            )
            
            # Subir imagen si existe
            if 'imagen' in request.FILES:
                imagen_file = request.FILES['imagen']
                ImagenProducto.objects.create(
                    producto=producto,
                    imagen=imagen_file,
                    es_principal=True
                )
            
            messages.success(request, f'Producto "{producto.titulo}" creado correctamente')
            return redirect('dashboard:productos_lista')
        except Exception as e:
            messages.error(request, 'Algo no salió bien. Avisale a Ramiro 🙂')
    
    return render(request, 'dashboard/producto_form.html', {'accion': 'Crear'})


@login_required
def producto_editar(request, producto_id):
    """Editar producto existente"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        try:
            precio = request.POST.get('precio')
            producto.titulo = request.POST.get('titulo')
            producto.descripcion = request.POST.get('descripcion')
            producto.precio = float(precio) if precio else None
            producto.precio_desde = request.POST.get('precio_desde') == 'on'
            producto.tiempo_estimado = request.POST.get('tiempo_estimado', '7-10 días')
            producto.activo = request.POST.get('activo') == 'on'
            producto.destacado = request.POST.get('destacado') == 'on'
            producto.save()
            
            # Subir nueva imagen si existe
            if 'imagen' in request.FILES:
                imagen_file = request.FILES['imagen']
                ImagenProducto.objects.create(
                    producto=producto,
                    imagen=imagen_file,
                    es_principal=True
                )
            
            messages.success(request, f'Producto "{producto.titulo}" actualizado correctamente')
            return redirect('dashboard:productos_lista')
        except Exception as e:
            messages.error(request, 'Algo no salió bien. Avisale a Ramiro 🙂')
    
    imagen_principal = producto.imagenes.filter(es_principal=True).first()
    if not imagen_principal:
        imagen_principal = producto.imagenes.first()
    
    context = {
        'producto': producto,
        'imagen_principal': imagen_principal,
        'accion': 'Editar',
    }
    return render(request, 'dashboard/producto_form.html', context)


@login_required
def producto_toggle_activo(request, producto_id):
    """Activar/desactivar producto"""
    producto = get_object_or_404(Producto, id=producto_id)
    try:
        producto.activo = not producto.activo
        producto.save()
        estado = "activado" if producto.activo else "desactivado"
        messages.success(request, f'Producto {estado} correctamente')
    except Exception as e:
        messages.error(request, 'Algo no salió bien. Avisale a Ramiro 🙂')
    return redirect('dashboard:productos_lista')


@login_required
def pedidos_lista(request):
    """Lista de pedidos"""
    estado_filtro = request.GET.get('estado', '')
    pedidos = Pedido.objects.all().order_by('-fecha_creacion')
    
    if estado_filtro:
        pedidos = pedidos.filter(estado=estado_filtro)
    
    # Obtener configuración para WhatsApp
    config_pedido = ConfiguracionPedido.objects.filter(activo=True).first()
    whatsapp_destino = config_pedido.whatsapp_destino if config_pedido else '5491155947837'
    
    context = {
        'pedidos': pedidos,
        'estado_filtro': estado_filtro,
        'estados': ESTADO_CHOICES,
        'whatsapp_destino': whatsapp_destino,
    }
    return render(request, 'dashboard/pedidos_lista.html', context)


@login_required
def pedido_actualizar_estado(request, pedido_id):
    """Actualizar estado de un pedido"""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        try:
            nuevo_estado = request.POST.get('estado')
            if nuevo_estado:
                pedido.estado = nuevo_estado
                pedido.save()
                messages.success(request, f'Estado del pedido actualizado a "{pedido.get_estado_display()}"')
        except Exception as e:
            messages.error(request, 'Algo no salió bien. Avisale a Ramiro 🙂')
    
    return redirect('dashboard:pedidos_lista')


@login_required
def pedido_actualizar_notas(request, pedido_id):
    """Actualizar notas internas de un pedido"""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        try:
            pedido.notas_internas = request.POST.get('notas_internas', '')
            pedido.save()
            messages.success(request, 'Notas internas guardadas')
        except Exception as e:
            messages.error(request, 'Algo no salió bien. Avisale a Ramiro 🙂')
    
    return redirect('dashboard:pedidos_lista')


@login_required
def configuracion_sitio(request):
    """Configuración general del sitio"""
    config = ConfiguracionSitio.get_config()
    
    if request.method == 'POST':
        try:
            config.whatsapp_sitio = request.POST.get('whatsapp_sitio', '5491155947837')
            config.instagram = request.POST.get('instagram', 'cami.zco')
            config.texto_boton_pedido = request.POST.get('texto_boton_pedido', 'Hacé tu pedido')
            config.banner_activo = request.POST.get('banner_activo') == 'on'
            config.banner_texto = request.POST.get('banner_texto', '')
            config.save()
            messages.success(request, 'Configuración guardada correctamente')
            return redirect('dashboard:configuracion_sitio')
        except Exception as e:
            messages.error(request, 'Algo no salió bien. Avisale a Ramiro 🙂')
    
    context = {
        'config': config,
    }
    return render(request, 'dashboard/configuracion_sitio.html', context)

