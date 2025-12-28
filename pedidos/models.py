from django.db import models
from django.utils import timezone


ESTADO_CHOICES = [
    ('nuevo', 'Nuevo'),
    ('confirmado', 'Confirmado'),
    ('en_produccion', 'En producción'),
    ('listo', 'Listo'),
    ('entregado', 'Entregado'),
]

ENTREGA_CHOICES = [
    ('retiro', 'Retiro'),
    ('envio', 'Envío'),
]


class ConfiguracionPedido(models.Model):
    """Configuración autogestionable para el flujo de pedidos"""
    whatsapp_destino = models.CharField(
        max_length=20, 
        default="5491112345678",
        help_text="Número de WhatsApp para recibir pedidos (ej: 5491112345678)"
    )
    tiempo_entrega = models.CharField(
        max_length=100,
        default="7-10 días",
        help_text="Texto de tiempo estimado de entrega (ej: 7-10 días)"
    )
    tiempo_respuesta = models.CharField(
        max_length=100,
        default="24-48 horas",
        help_text="Tiempo estimado de respuesta por WhatsApp (ej: 24-48 horas)"
    )
    texto_confirmacion = models.TextField(
        blank=True,
        help_text="Texto opcional para la página de confirmación"
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Configuración de Pedidos'
        verbose_name_plural = 'Configuración de Pedidos'

    def __str__(self):
        return "Configuración de Pedidos"
    
    def save(self, *args, **kwargs):
        # Solo permitir un registro activo
        if self.activo:
            ConfiguracionPedido.objects.filter(activo=True).exclude(pk=self.pk).update(activo=False)
        super().save(*args, **kwargs)


class Pedido(models.Model):
    nombre = models.CharField(max_length=200)
    whatsapp = models.CharField(max_length=20)
    producto = models.ForeignKey('catalogo.Producto', on_delete=models.SET_NULL, null=True, blank=True)
    texto_tallar = models.TextField(blank=True, help_text="Texto que el cliente quiere tallar (opcional pero recomendado)")
    cantidad = models.PositiveIntegerField(default=1)
    fecha_para_cuando = models.DateField(null=True, blank=True, verbose_name="Fecha para cuándo", help_text="¿Para cuándo lo necesitás?")
    entrega = models.CharField(max_length=10, choices=ENTREGA_CHOICES, default='retiro')
    zona_ciudad = models.CharField(max_length=200, blank=True, verbose_name="Zona / Ciudad", help_text="Solo si elegiste envío")
    notas = models.TextField(blank=True, help_text="Algo más a tener en cuenta")
    notas_internas = models.TextField(blank=True, help_text="Notas internas (solo visible en el panel)")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='nuevo')
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    fecha_actualizacion = models.DateTimeField(default=timezone.now, editable=False)
    
    # Campo para honeypot (anti-spam)
    website = models.CharField(max_length=200, blank=True, help_text="Campo honeypot - no completar")

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre}"

    def save(self, *args, **kwargs):
        if self.pk:
            self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)
    
    def get_estado_display_class(self):
        """Retorna clase CSS para el estado"""
        clases = {
            'nuevo': 'badge-nuevo',
            'confirmado': 'badge-confirmado',
            'en_produccion': 'badge-produccion',
            'listo': 'badge-listo',
            'entregado': 'badge-entregado',
        }
        return clases.get(self.estado, '')
    
    def get_mensaje_whatsapp(self):
        """Genera el mensaje prearmado para WhatsApp"""
        mensaje = f"Hola! Soy {self.nombre}.\n\n"
        mensaje += f"Quiero hacer un pedido:\n"
        
        if self.producto:
            mensaje += f"• Producto: {self.producto.titulo}\n"
        else:
            mensaje += f"• Producto: Personalizado\n"
        
        mensaje += f"• Cantidad: {self.cantidad}\n"
        
        if self.texto_tallar:
            mensaje += f"• Texto a grabar: {self.texto_tallar}\n"
        
        mensaje += f"• Entrega: {self.get_entrega_display()}\n"
        
        if self.entrega == 'envio' and self.zona_ciudad:
            mensaje += f"• Zona/Ciudad: {self.zona_ciudad}\n"
        
        if self.fecha_para_cuando:
            mensaje += f"• Para cuándo: {self.fecha_para_cuando.strftime('%d/%m/%Y')}\n"
        
        if self.notas:
            mensaje += f"• Notas: {self.notas}\n"
        
        mensaje += f"\nMi WhatsApp: {self.whatsapp}"
        
        # Codificar para URL
        from urllib.parse import quote
        return quote(mensaje)
