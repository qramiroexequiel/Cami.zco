from django.urls import path
from . import views

app_name = 'contacto'

urlpatterns = [
    path('consulta/', views.crear_consulta, name='crear'),
    path('consulta/confirmacion/', views.confirmacion_consulta, name='confirmacion'),
]

