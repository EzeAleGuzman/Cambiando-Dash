from django.views.generic import ListView, DetailView
from .models import Documento, VersionDocumento


class DocumentoListView(ListView):
    model = Documento
    template_name = (
        "ProtocolosDigitales/documento_list.html"  # Aquí especificas la ruta completa
    )
    context_object_name = "documentos"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DocumentoDetailView(DetailView):
    model = Documento
    template_name = "ProtocolosDigitales/documento_detail.html"
    context_object_name = "documento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["versiones"] = (
            self.object.versiones.all()
        )  # Obtener todas las versiones del documento
        return context


class VersionDocumentoDetailView(DetailView):
    model = VersionDocumento
    template_name = "ProtocolosDigitales/versiondocumento_detail.html"
    context_object_name = "version"
