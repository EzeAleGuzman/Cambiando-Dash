from django.contrib import admin
from .models import Documento, VersionDocumento


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "clase", "codigo")
    ordering = ("nombre",)


class VersionDocumentoInline(admin.TabularInline):
    model = VersionDocumento
    extra = 0


admin.site.register(Documento, DocumentoAdmin)
admin.site.register(VersionDocumento)
