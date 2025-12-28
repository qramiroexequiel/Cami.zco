from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponse
from django.db import OperationalError
import csv
from .models import Pedido, ConfiguracionPedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'whatsapp', 'producto', 'cantidad', 'estado', 'estado_badge', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion', 'producto')
    search_fields = ('nombre', 'whatsapp', 'texto_tallar')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    list_editable = ('estado',)
    actions = ['exportar_csv']

    fieldsets = (
        ('Información del cliente', {
            'fields': ('nombre', 'whatsapp')
        }),
        ('Detalles del pedido', {
            'fields': ('producto', 'cantidad', 'texto_tallar', 'fecha_para_cuando', 'entrega', 'zona_ciudad', 'notas')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def estado_badge(self, obj):
        clases = {
            'nuevo': 'background-color: #dbeafe; color: #1e40af;',
            'confirmado': 'background-color: #fef3c7; color: #92400e;',
            'en_produccion': 'background-color: #fce7f3; color: #9f1239;',
            'listo': 'background-color: #d1fae5; color: #065f46;',
            'entregado': 'background-color: #dcfce7; color: #166534;',
        }
        estilo = clases.get(obj.estado, '')
        return format_html(
            '<span style="{} padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 500;">{}</span>',
            estilo,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'

    def exportar_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="pedidos.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Nombre', 'WhatsApp', 'Producto', 'Texto a tallar', 
            'Cantidad', 'Fecha para cuándo', 'Entrega', 'Zona/Ciudad', 'Notas', 'Estado', 'Fecha creación'
        ])
        
        for pedido in queryset:
            writer.writerow([
                pedido.id,
                pedido.nombre,
                pedido.whatsapp,
                pedido.producto.titulo if pedido.producto else 'Personalizado',
                pedido.texto_tallar,
                pedido.cantidad,
                pedido.fecha_para_cuando.strftime('%d/%m/%Y') if pedido.fecha_para_cuando else '',
                pedido.get_entrega_display(),
                pedido.zona_ciudad,
                pedido.notas,
                pedido.get_estado_display(),
                pedido.fecha_creacion.strftime('%d/%m/%Y %H:%M')
            ])
        
        return response
    
    exportar_csv.short_description = "Exportar seleccionados a CSV"


@admin.register(ConfiguracionPedido)
class ConfiguracionPedidoAdmin(admin.ModelAdmin):
    list_display = ('whatsapp_destino', 'tiempo_entrega', 'tiempo_respuesta', 'activo')
    
    fieldsets = (
        ('WhatsApp', {
            'fields': ('whatsapp_destino',),
            'description': 'Número de WhatsApp donde recibirás los pedidos (ej: 5491112345678)'
        }),
        ('Textos', {
            'fields': ('tiempo_entrega', 'tiempo_respuesta', 'texto_confirmacion')
        }),
        ('Configuración', {
            'fields': ('activo',)
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir un registro
        # Usar try/except para evitar errores si la tabla no existe aún
        try:
            if ConfiguracionPedido.objects.exists():
                return False
        except OperationalError:
            # Si la tabla no existe, permitir crear el primer registro
            pass
        return super().has_add_permission(request)
