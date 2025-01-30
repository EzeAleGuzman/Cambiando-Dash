from django.contrib import admin
from .models import Servicio, Ubicacion, Cama, PacienteCama


class CamasInline(admin.TabularInline):
    model = Cama
    extra = 2

class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "descripcion",
        "color_identificativo",
        "orden_visualizacion",
        "capacidad_total",
        "nivel_alerta_ocupacion",
        "activo",
    )
    list_filter = ("activo",)
    search_fields = (
        "nombre",
        "descripcion",
        "color_identificativo",
        "orden_visualizacion",
        "capacidad_total",
        "nivel_alerta_ocupacion",
    )
    ordering = ("nombre",)
    


class UbicacionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "capacidad", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "tipo", "capacidad")
    ordering = ("nombre",)
    inlines = [CamasInline]


class CamaAdmin(admin.ModelAdmin):
    list_display = ("numero", "estado", "activo", "ubicacion",'get_servicio',"notas")
    list_filter = ("activo",)
    search_fields = ("numero", "estado")
    ordering = ('ubicacion__servicio__nombre', "ubicacion__nombre", "numero")

    def get_servicio(self, obj):
        return obj.ubicacion.servicio.nombre
    get_servicio.short_description = 'Servicio'
    get_servicio.admin_order_field = 'ubicacion__servicio__nombre'

class PacienteCamaAdmin(admin.ModelAdmin):
    list_display = ("paciente", "cama", "fecha_liberacion", "fecha_asignacion")
    search_fields = ("numero", "estado")


admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Ubicacion, UbicacionAdmin)
admin.site.register(Cama, CamaAdmin)
admin.site.register(PacienteCama, PacienteCamaAdmin)