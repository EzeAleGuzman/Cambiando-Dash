from django.urls import path
from .views import DocumentoListView, DocumentoDetailView, VersionDocumentoDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("documentos/", DocumentoListView.as_view(), name="documento_list"),
    path(
        "documentos/<int:pk>/", DocumentoDetailView.as_view(), name="documento_detail"
    ),
    path(
        "versiones/<int:pk>/",
        VersionDocumentoDetailView.as_view(),
        name="version_detail",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
