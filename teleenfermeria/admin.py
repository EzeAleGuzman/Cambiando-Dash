from django.contrib import admin
from .models import Teleseguimiento, Seguimiento

app_name = "teleenfermeria"


class TeleseguimientoAdmin(admin.ModelAdmin):
    list_display = ("paciente", "fecha_solicitud", "estado")
    list_filter = ("estado",)
    fields = (
        "paciente",
        "fecha_solicitud",
        "descripcion",
        "condicion",
        "consentimiento_seguimiento",
        "estado",
        "diagnostico",
        "medicaciones",
    )
    readonly_fields = (
        "paciente",
    )  # Si deseas que el campo paciente sea solo de lectura


admin.site.register(Teleseguimiento, TeleseguimientoAdmin)
admin.site.register(Seguimiento)
