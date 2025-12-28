from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('pedir/', views.crear_pedido, name='crear'),
    path('pedir/<slug:producto_slug>/', views.crear_pedido, name='crear_con_producto'),
    path('confirmacion/<int:pedido_id>/', views.confirmacion_pedido, name='confirmacion'),
]

