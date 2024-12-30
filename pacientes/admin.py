from django.contrib import admin
from .models import Registro, Paciente

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'fecha_nacimiento', 'genero', 'direccion', 'telefono', 'email')
    list_filter = ('genero',)
    search_fields = ('nombre', 'apellido', 'dni', 'email')
    ordering = ('nombre',)

admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Registro)
