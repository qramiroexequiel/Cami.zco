from django.contrib import admin
from .models import (
    Categoria, Producto, ImagenProducto, SeccionHome, ImagenSeccion,
    HeroHome, PasoProceso, GaleriaTrabajo, PreguntaFrecuente, CTAFinal,
    ConfiguracionSitio
)


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    fields = ('imagen', 'orden', 'es_principal')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre',)
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'get_precio_display', 'activo', 'destacado', 'fecha_creacion')
    list_filter = ('activo', 'destacado', 'categoria', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [ImagenProductoInline]
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'slug', 'descripcion', 'categoria')
        }),
        ('Precio y disponibilidad', {
            'fields': ('precio', 'precio_desde', 'tiempo_estimado', 'activo', 'destacado', 'orden')
        }),
    )


@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'orden', 'es_principal')
    list_filter = ('es_principal',)
    search_fields = ('producto__titulo',)


class ImagenSeccionInline(admin.TabularInline):
    model = ImagenSeccion
    extra = 1
    fields = ('imagen', 'alt_text', 'tipo', 'orden', 'activa')
    verbose_name = 'Imagen'
    verbose_name_plural = 'Imágenes de la sección'
    help_text = 'Puedes agregar múltiples imágenes. La primera será la principal que se muestra en la sección.'


@admin.register(SeccionHome)
class SeccionHomeAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'titulo', 'activa', 'orden')
    list_filter = ('activa', 'tipo')
    search_fields = ('titulo', 'texto')
    inlines = [ImagenSeccionInline]
    fieldsets = (
        ('Información básica', {
            'fields': ('tipo', 'titulo', 'texto')
        }),
        ('Configuración', {
            'fields': ('activa', 'orden')
        }),
    )


@admin.register(ImagenSeccion)
class ImagenSeccionAdmin(admin.ModelAdmin):
    list_display = ('get_tipo_display', 'alt_text', 'seccion', 'orden', 'activa')
    list_filter = ('tipo', 'activa', 'seccion')
    search_fields = ('alt_text', 'seccion__titulo')
    fieldsets = (
        ('Imagen', {
            'fields': ('imagen', 'alt_text', 'tipo')
        }),
        ('Asociación', {
            'fields': ('seccion',)
        }),
        ('Configuración', {
            'fields': ('orden', 'activa')
        }),
    )


@admin.register(HeroHome)
class HeroHomeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'fecha_actualizacion')
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'subtitulo', 'texto_boton', 'url_cta')
        }),
        ('Imágenes', {
            'fields': ('imagen_fondo', 'logo'),
            'description': 'Sube una imagen de fondo y el logo. Si no subes imagen de fondo, se usará un gradiente.'
        }),
        ('Configuración', {
            'fields': ('activo',)
        }),
    )


@admin.register(PasoProceso)
class PasoProcesoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'titulo', 'orden', 'activo')
    list_filter = ('activo',)
    search_fields = ('titulo', 'descripcion')
    fieldsets = (
        ('Contenido', {
            'fields': ('numero', 'titulo', 'descripcion', 'icono')
        }),
        ('Configuración', {
            'fields': ('orden', 'activo')
        }),
    )


@admin.register(GaleriaTrabajo)
class GaleriaTrabajoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'alt_text', 'orden', 'activa', 'fecha_creacion')
    list_filter = ('activa', 'fecha_creacion')
    search_fields = ('titulo', 'alt_text')
    fieldsets = (
        ('Imagen', {
            'fields': ('imagen', 'alt_text', 'titulo')
        }),
        ('Configuración', {
            'fields': ('orden', 'activa')
        }),
    )


@admin.register(PreguntaFrecuente)
class PreguntaFrecuenteAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'orden', 'activa')
    list_filter = ('activa',)
    search_fields = ('pregunta', 'respuesta')
    fieldsets = (
        ('Contenido', {
            'fields': ('pregunta', 'respuesta')
        }),
        ('Configuración', {
            'fields': ('orden', 'activa')
        }),
    )


@admin.register(CTAFinal)
class CTAFinalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo')
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'texto', 'texto_boton', 'url_cta'),
            'description': 'Puedes usar una URL relativa (ej: /pedir/) o una URL completa (ej: https://wa.me/5491112345678 para WhatsApp directo)'
        }),
        ('Configuración', {
            'fields': ('activo',)
        }),
    )


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'whatsapp_sitio', 'instagram')
    
    fieldsets = (
        ('Redes Sociales', {
            'fields': ('instagram', 'instagram_url', 'whatsapp_sitio', 'whatsapp_numero', 'whatsapp_mensaje'),
            'description': 'Configuración de enlaces a redes sociales. Instagram URL es la URL completa del perfil.'
        }),
        ('Configuración General', {
            'fields': ('texto_boton_pedido', 'banner_activo', 'banner_texto', 'notas_internas_pedidos')
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir un registro (singleton)
        if ConfiguracionSitio.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar la configuración
        return False
