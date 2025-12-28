from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.CatalogoListView.as_view(), name='lista'),
    path('<slug:slug>/', views.ProductoDetailView.as_view(), name='detalle'),
    path('galeria/', views.galeria_completa, name='galeria_completa'),
    path('preguntas-frecuentes/', views.faq_completa, name='faq_completa'),
]

