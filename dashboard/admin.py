from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseForbidden


class CustomAdminSite(AdminSite):
    """Admin site personalizado que bloquea acceso a usuarios normales"""
    
    def has_permission(self, request):
        """Solo superusuarios pueden acceder al Django Admin"""
        return request.user.is_active and request.user.is_superuser


# Crear instancia personalizada del admin
custom_admin_site = CustomAdminSite(name='admin')

# Registrar modelos solo para superusuarios
custom_admin_site.register(User, UserAdmin)

