from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("internos.urls")),
    path("", include("ProtocolosDigitales.urls")),
    path("", include("gestioncamas.urls")),
    path("", include("pacientes.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
