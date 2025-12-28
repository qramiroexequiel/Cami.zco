from django.contrib import admin
from .models import Consulta


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'whatsapp', 'fecha_creacion', 'leida')
    list_filter = ('leida', 'fecha_creacion')
    search_fields = ('nombre', 'whatsapp', 'mensaje')
    readonly_fields = ('fecha_creacion',)
    list_editable = ('leida',)
    
    fieldsets = (
        ('Información del contacto', {
            'fields': ('nombre', 'whatsapp')
        }),
        ('Mensaje', {
            'fields': ('mensaje',)
        }),
        ('Estado', {
            'fields': ('leida',)
        }),
        ('Fecha', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )
