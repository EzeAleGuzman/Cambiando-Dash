from django.contrib import admin
from .models import Aislamiento, TipoAislamiento

# Register your models here.
class Aislamientoadmin(admin.ModelAdmin):
    list_display = ('cama_paciente', 'tipo', 'fecha_inicio', 'fecha_fin')

admin.site.register(Aislamiento, Aislamientoadmin)
admin.site.register(TipoAislamiento)