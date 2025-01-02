from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Interno


# Register your models here.
class InternoAdmin(ImportExportModelAdmin):
    list_display = ("servicio", "interno")
    search_fields = ("servicio", "interno")


admin.site.register(Interno, InternoAdmin)
