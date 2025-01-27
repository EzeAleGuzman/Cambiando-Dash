from django.contrib import admin
from .models import Teleseguimiento, Seguimiento, Medicacion, Prescripcion

app_name = "teleenfermeria"


class PrescripcionInline(admin.TabularInline):
    model = Prescripcion
    extra = 1


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
    )
    readonly_fields = (
        "paciente",
    )  # Si deseas que el campo paciente sea solo de lectura
    inlines = [PrescripcionInline]


admin.site.site_header = "Administración de Teleenfermería"
admin.site.register(Teleseguimiento, TeleseguimientoAdmin)
admin.site.register(Seguimiento)
admin.site.register(Medicacion)
admin.site.register(Prescripcion)
