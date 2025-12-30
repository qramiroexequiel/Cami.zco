from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db import models
from urllib.parse import quote
from .models import (
    Producto, Categoria, SeccionHome, ImagenSeccion,
    HeroHome, PasoProceso, GaleriaTrabajo, PreguntaFrecuente, CTAFinal
)


def home(request):
    """Vista de la landing page"""
    productos_destacados = Producto.objects.filter(
        activo=True, 
        destacado=True
    ).select_related('categoria').prefetch_related('imagenes')[:6]
    
    total_destacados = Producto.objects.filter(activo=True, destacado=True).count()
    hay_mas_destacados = total_destacados > 6
    
    categorias = Categoria.objects.filter(activa=True)
    hero = HeroHome.objects.filter(activo=True).first()
    
    seccion_nuestro_trabajo = SeccionHome.objects.filter(
        tipo='nuestro_trabajo',
        activa=True
    ).prefetch_related(
        models.Prefetch(
            'imagenes',
            queryset=ImagenSeccion.objects.filter(activa=True).order_by('orden')
        )
    ).first()
    
    pasos = PasoProceso.objects.filter(activo=True).order_by('orden', 'numero')[:3]
    galeria = GaleriaTrabajo.objects.filter(activa=True).order_by('orden', '-fecha_creacion')[:9]
    
    total_trabajos = GaleriaTrabajo.objects.filter(activa=True).count()
    hay_mas_trabajos = total_trabajos > 9
    
    faqs = PreguntaFrecuente.objects.filter(activa=True).order_by('orden')[:6]
    total_faqs = PreguntaFrecuente.objects.filter(activa=True).count()
    hay_mas_faqs = total_faqs > 6
    
    cta_final = CTAFinal.objects.filter(activo=True).first()
    
    context = {
        'productos_destacados': productos_destacados,
        'hay_mas_destacados': hay_mas_destacados,
        'categorias': categorias,
        'hero': hero,
        'seccion_nuestro_trabajo': seccion_nuestro_trabajo,
        'pasos': pasos,
        'galeria': galeria,
        'hay_mas_trabajos': hay_mas_trabajos,
        'faqs': faqs,
        'hay_mas_faqs': hay_mas_faqs,
        'cta_final': cta_final,
    }
    return render(request, 'home.html', context)


class CatalogoListView(ListView):
    model = Producto
    template_name = 'catalogo/lista.html'
    context_object_name = 'productos'
    paginate_by = 12

    def get_queryset(self):
        queryset = Producto.objects.filter(activo=True).select_related('categoria').prefetch_related('imagenes')
        categoria_slug = self.request.GET.get('categoria')
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.filter(activa=True)
        context['categoria_actual'] = self.request.GET.get('categoria')
        return context


class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'catalogo/detalle.html'
    context_object_name = 'producto'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Producto.objects.filter(activo=True).prefetch_related('imagenes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.categoria:
            context['productos_relacionados'] = Producto.objects.filter(
                activo=True,
                categoria=self.object.categoria
            ).exclude(id=self.object.id)[:4]
        
        from pedidos.models import ConfiguracionPedido
        config = ConfiguracionPedido.objects.filter(activo=True).first()
        
        if config:
            url_producto = self.request.build_absolute_uri(self.object.get_absolute_url())
            mensaje = self.object.get_mensaje_whatsapp_consulta(url_producto)
            mensaje_codificado = quote(mensaje)
            whatsapp_url = f"https://wa.me/{config.whatsapp_destino}?text={mensaje_codificado}"
            context['whatsapp_url'] = whatsapp_url
            context['config_whatsapp'] = config
        
        context['seo_title'] = self.object.get_seo_title()
        context['seo_description'] = self.object.get_seo_description()
        context['og_image_url'] = self.object.get_og_image_url(self.request)
        context['og_url'] = self.request.build_absolute_uri(self.object.get_absolute_url())
        
        return context


def galeria_completa(request):
    """Vista para mostrar la galería completa de trabajos"""
    trabajos = GaleriaTrabajo.objects.filter(activa=True).order_by('orden', '-fecha_creacion')
    
    context = {
        'trabajos': trabajos,
    }
    return render(request, 'catalogo/galeria_completa.html', context)


def faq_completa(request):
    """Vista para mostrar todas las preguntas frecuentes"""
    faqs = PreguntaFrecuente.objects.filter(activa=True).order_by('orden')
    
    context = {
        'faqs': faqs,
    }
    return render(request, 'catalogo/faq_completa.html', context)
