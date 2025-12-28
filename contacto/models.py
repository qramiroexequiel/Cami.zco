from django.db import models


class Consulta(models.Model):
    nombre = models.CharField(max_length=200)
    whatsapp = models.CharField(max_length=20)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def __str__(self):
        return f"Consulta de {self.nombre} - {self.fecha_creacion.strftime('%d/%m/%Y')}"
