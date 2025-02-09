from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import PacienteResource
from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(ImportExportModelAdmin):
    resource_class = PacienteResource
    ordering = ["nombre_completo"]
    search_fields = ["nombre_completo", "dni"]
