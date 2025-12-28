from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('productos/', views.productos_lista, name='productos_lista'),
    path('productos/crear/', views.producto_crear, name='producto_crear'),
    path('productos/<int:producto_id>/editar/', views.producto_editar, name='producto_editar'),
    path('productos/<int:producto_id>/toggle/', views.producto_toggle_activo, name='producto_toggle_activo'),
    path('pedidos/', views.pedidos_lista, name='pedidos_lista'),
    path('pedidos/<int:pedido_id>/estado/', views.pedido_actualizar_estado, name='pedido_actualizar_estado'),
    path('pedidos/<int:pedido_id>/notas/', views.pedido_actualizar_notas, name='pedido_actualizar_notas'),
    path('configuracion/', views.configuracion_sitio, name='configuracion_sitio'),
]

