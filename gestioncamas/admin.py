from django.contrib import admin
from .models import Servicio, Ubicacion, Cama

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'color_identificativo', 'orden_visualizacion', 'capacidad_total', 'nivel_alerta_ocupacion', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion', 'color_identificativo', 'orden_visualizacion', 'capacidad_total', 'nivel_alerta_ocupacion')
    ordering = ('nombre',)

class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'capacidad', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'tipo', 'capacidad')
    ordering = ('nombre',)

class CamaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'estado', 'activo', 'ubicacion', 'notas' )
    list_filter = ('activo',)
    search_fields = ('numero', 'estado')
    ordering = ('numero',)



admin.site.register(Servicio)
admin.site.register(Ubicacion)
admin.site.register(Cama, CamaAdmin)



