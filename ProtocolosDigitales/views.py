from django.views.generic import ListView, DetailView
from .models import Documento, VersionDocumento
import openai
import PyPDF2
from django.shortcuts import render
from django.http import JsonResponse
import os
from .key import api_key


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


# Función para extraer texto del PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        lector = PyPDF2.PdfReader(file)
        texto = ""
        for pagina in lector.pages:
            texto += pagina.extract_text()
    return texto


def chat_pdf(request):
    if request.method == "POST":
        documento_id = request.POST.get("documento_id")
        question = request.POST.get("question")

        if not documento_id or not question:
            return JsonResponse(
                {"error": "Documento ID and question are required."}, status=400
            )

        try:
            documento = VersionDocumento.objects.get(id=documento_id)
        except VersionDocumento.DoesNotExist:
            return JsonResponse({"error": "Documento not found."}, status=404)

        # Extraer el texto del PDF
        texto_del_documento = extract_text_from_pdf(documento.archivo_pdf.path)

        # Define el prompt que quieres enviar al modelo
        prompt = (
            f"Este es el contenido del documento:\n\n{texto_del_documento}\n\n"
            f"Por favor, responde solo sobre el contenido del documento anterior.\n\n"
            f"Si la consulta es distinta a lo que se encuentra en el documento, Contesta que es no se puede utilizar el servicio para esto"
            f"Pregunta: {question}"
        )

        # Configura la clave de API
        openai.api_key = api_key

        # Realiza la solicitud a la API de OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )

        # Obtén la respuesta del modelo
        answer = response.choices[0].message["content"].strip()

        return JsonResponse({"answer": answer})

    return JsonResponse({"error": "Invalid request method."}, status=405)
