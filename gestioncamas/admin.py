from django.contrib import admin
from .models import Servicio, Ubicacion, Cama, PacienteCama


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


class CamaAdmin(admin.ModelAdmin):
    list_display = ("numero", "estado", "activo", "ubicacion", "notas")
    list_filter = ("activo",)
    search_fields = ("numero", "estado")
    ordering = ("numero",)

class PacienteCamaAdmin(admin.ModelAdmin):
    list_display = ("paciente", "cama", "fecha_liberacion", "fecha_asignacion")
    search_fields = ("numero", "estado")


admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Ubicacion, UbicacionAdmin)
admin.site.register(Cama, CamaAdmin)
admin.site.register(PacienteCama, PacienteCamaAdmin)