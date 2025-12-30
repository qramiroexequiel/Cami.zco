from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Producto(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_desde = models.BooleanField(default=False, help_text="Si está marcado, muestra 'Desde $X' en lugar del precio fijo")
    tiempo_estimado = models.CharField(max_length=50, default="7-10 días", help_text="Ej: '7-10 días', '2 semanas'")
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False, help_text="Aparece en la home")
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    fecha_actualizacion = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ['orden', '-fecha_creacion']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        if self.pk:
            self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)

    def get_precio_display(self):
        if self.precio_desde and self.precio:
            return f"Desde ${self.precio}"
        elif self.precio:
            return f"${self.precio}"
        return "Consultar precio"
    
    def get_absolute_url(self):
        """Retorna la URL absoluta del producto"""
        from django.urls import reverse
        return reverse('catalogo:detalle', kwargs={'slug': self.slug})
    
    def get_mensaje_whatsapp_consulta(self, url_producto):
        """Genera el mensaje prearmado para consulta rápida por WhatsApp"""
        mensaje = f"Hola! Vi este producto en tu web y quería consultarte:\n\n"
        mensaje += f"Producto: {self.titulo}\n"
        mensaje += f"Link: {url_producto}\n"
        return mensaje
    
    def get_seo_title(self):
        """Genera el título SEO para el producto"""
        return f"Vasos grabados personalizados – {self.titulo}"
    
    def get_seo_description(self):
        """Genera la meta description SEO para el producto"""
        if self.descripcion:
            descripcion_limpia = self.descripcion.strip()
            descripcion_limpia = ' '.join(descripcion_limpia.split())
            if len(descripcion_limpia) > 155:
                descripcion_limpia = descripcion_limpia[:152] + "..."
            return descripcion_limpia
        tipo_producto = "vaso o copa"
        if self.categoria:
            nombre_categoria = self.categoria.nombre.lower()
            if "vaso" in nombre_categoria:
                tipo_producto = "vaso"
            elif "copa" in nombre_categoria:
                tipo_producto = "copa"
            elif "set" in nombre_categoria:
                tipo_producto = "set"
        
        return f"{self.titulo}. Grabado a mano personalizado. {tipo_producto.capitalize()} único con diseño personalizado para momentos especiales."
    
    def get_og_image_url(self, request=None):
        """Retorna la URL absoluta de la imagen principal del producto para Open Graph"""
        imagen_principal = self.imagenes.filter(es_principal=True).first()
        if not imagen_principal:
            imagen_principal = self.imagenes.first()
        
        if imagen_principal and imagen_principal.imagen:
            if request:
                return request.build_absolute_uri(imagen_principal.imagen.url)
            return imagen_principal.imagen.url
        
        # Fallback: retornar None si no hay imagen (el template manejará esto)
        return None


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', verbose_name='imagen')
    orden = models.PositiveIntegerField(default=0)
    es_principal = models.BooleanField(default=False)

    class Meta:
        ordering = ['es_principal', 'orden']
        verbose_name = 'Imagen de Producto'
        verbose_name_plural = 'Imágenes de Productos'

    def __str__(self):
        return f"{self.producto.titulo} - Imagen {self.orden}"


class SeccionHome(models.Model):
    """Modelo para gestionar secciones de contenido en la home"""
    TIPO_CHOICES = [
        ('nuestro_trabajo', 'Nuestro Trabajo'),
        ('proceso', 'Proceso'),
        ('testimoniales', 'Testimoniales'),
        ('otro', 'Otro'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='nuestro_trabajo', unique=True)
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    activa = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    fecha_actualizacion = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ['orden', 'tipo']
        verbose_name = 'Sección Home'
        verbose_name_plural = 'Secciones Home'

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"

    def save(self, *args, **kwargs):
        if self.pk:
            self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)


class ImagenSeccion(models.Model):
    """Modelo reutilizable para gestionar imágenes de diferentes secciones"""
    TIPO_CHOICES = [
        ('proceso', 'Proceso de trabajo'),
        ('trabajo_real', 'Trabajo real'),
        ('logo', 'Logo'),
        ('persona_trabajando', 'Persona trabajando'),
        ('cliente', 'Cliente'),
        ('evento', 'Evento'),
        ('temporada', 'Temporada'),
        ('hero', 'Hero / Imagen principal'),
        ('otro', 'Otro'),
    ]
    
    seccion = models.ForeignKey(SeccionHome, related_name='imagenes', on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='proceso')
    imagen = models.ImageField(upload_to='secciones/', verbose_name='imagen')
    alt_text = models.CharField(max_length=200, help_text="Texto alternativo para accesibilidad")
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ['orden', '-fecha_creacion']
        verbose_name = 'Imagen de Sección'
        verbose_name_plural = 'Imágenes de Secciones'

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.alt_text[:50]}"


class HeroHome(models.Model):
    """Modelo para gestionar el Hero de la home"""
    imagen_fondo = models.ImageField(upload_to='hero/', null=True, blank=True, verbose_name='imagen_fondo', help_text="Imagen de fondo del hero")
    logo = models.ImageField(upload_to='logo/', null=True, blank=True, verbose_name='logo', help_text="Logo de la marca")
    titulo = models.CharField(max_length=200, default="Vasos Tallados Personalizados")
    subtitulo = models.CharField(max_length=300, default="Diseños únicos para momentos especiales")
    texto_boton = models.CharField(max_length=50, default="Hacé tu pedido")
    url_cta = models.CharField(max_length=200, default="/pedir/", help_text="URL del botón CTA (ej: /pedir/ o URL completa)")
    activo = models.BooleanField(default=True)
    fecha_actualizacion = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        verbose_name = 'Hero Home'
        verbose_name_plural = 'Hero Home'

    def __str__(self):
        return f"Hero - {self.titulo}"

    def save(self, *args, **kwargs):
        if self.pk:
            self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)


class PasoProceso(models.Model):
    """Modelo para gestionar los pasos del proceso (Cómo funciona)"""
    numero = models.PositiveIntegerField(default=1)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, blank=True, help_text="Emoji o código de icono (ej: ✨, 1, etc.)")
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'numero']
        verbose_name = 'Paso del Proceso'
        verbose_name_plural = 'Pasos del Proceso'

    def __str__(self):
        return f"Paso {self.numero}: {self.titulo}"


class GaleriaTrabajo(models.Model):
    """Modelo para la galería de trabajos reales"""
    imagen = models.ImageField(upload_to='galeria/', verbose_name='imagen')
    titulo = models.CharField(max_length=200, blank=True, help_text="Título opcional para la imagen")
    alt_text = models.CharField(max_length=200, help_text="Texto alternativo para accesibilidad")
    activa = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ['orden', '-fecha_creacion']
        verbose_name = 'Imagen de Galería'
        verbose_name_plural = 'Galería de Trabajos'

    def __str__(self):
        return f"{self.titulo or 'Trabajo'} - {self.alt_text[:30]}"


class PreguntaFrecuente(models.Model):
    """Modelo para preguntas frecuentes"""
    pregunta = models.CharField(max_length=300)
    respuesta = models.TextField()
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'pregunta']
        verbose_name = 'Pregunta Frecuente'
        verbose_name_plural = 'Preguntas Frecuentes'

    def __str__(self):
        return self.pregunta[:50]


class CTAFinal(models.Model):
    """Modelo para el CTA final de la home"""
    titulo = models.CharField(max_length=200, default="¿Querés un regalo personalizado?")
    texto = models.TextField(blank=True, help_text="Texto opcional debajo del título")
    texto_boton = models.CharField(max_length=50, default="Hacé tu pedido")
    url_cta = models.CharField(max_length=200, default="/pedir/", help_text="URL del botón CTA (ej: /pedir/ o https://wa.me/5491112345678)")
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'CTA Final'
        verbose_name_plural = 'CTA Final'

    def __str__(self):
        return self.titulo


class ConfiguracionSitio(models.Model):
    """Configuración general del sitio (singleton)"""
    whatsapp_sitio = models.CharField(
        max_length=20,
        default="5491155947837",
        help_text="Número de WhatsApp que aparece en el sitio (ej: 5491155947837)"
    )
    instagram = models.CharField(
        max_length=100,
        default="cami.zco",
        help_text="Usuario de Instagram (sin @)"
    )
    texto_boton_pedido = models.CharField(
        max_length=100,
        default="Hacé tu pedido",
        help_text="Texto del botón principal de pedidos"
    )
    banner_activo = models.BooleanField(
        default=False,
        help_text="Activar banner temporal"
    )
    banner_texto = models.CharField(
        max_length=200,
        blank=True,
        help_text="Texto del banner (ej: 'Pedidos cerrados por vacaciones')"
    )
    notas_internas_pedidos = models.BooleanField(
        default=True,
        help_text="Mostrar campo de notas internas en pedidos"
    )
    instagram_url = models.URLField(
        blank=True,
        help_text="URL completa de Instagram (ej: https://instagram.com/cami.zco)"
    )
    whatsapp_numero = models.CharField(
        max_length=20,
        blank=True,
        help_text="Número de WhatsApp solo con números (ej: 5491155947837)"
    )
    whatsapp_mensaje = models.CharField(
        max_length=200,
        blank=True,
        default="Hola! Quiero hacer un pedido 😊",
        help_text="Mensaje predefinido para WhatsApp"
    )

    class Meta:
        verbose_name = 'Configuración del Sitio'
        verbose_name_plural = 'Configuración del Sitio'

    def __str__(self):
        return "Configuración del Sitio"
    
    def save(self, *args, **kwargs):
        # Singleton: solo permitir un registro
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        """Obtiene o crea la configuración única"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
