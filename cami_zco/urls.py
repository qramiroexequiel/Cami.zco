"""
URL configuration for cami.zco project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import user_passes_test
from catalogo import views as catalogo_views

# Bloquear acceso al Django Admin para usuarios normales
def is_superuser(user):
    return user.is_authenticated and user.is_superuser

# Proteger el admin site
admin.site.login = user_passes_test(is_superuser, login_url='/dashboard/')(admin.site.login)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', catalogo_views.home, name='home'),
    path('catalogo/', include('catalogo.urls')),
    path('', include('pedidos.urls')),
    path('', include('contacto.urls')),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
