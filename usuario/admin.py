from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'apellido', 'tipo_usuario', 'is_active', 'is_staff')
    search_fields = ('email', 'nombre', 'apellido')
