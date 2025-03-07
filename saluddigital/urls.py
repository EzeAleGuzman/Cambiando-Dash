from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from gestioncamas import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("admin/", admin.site.urls),
    path("", include("internos.urls")),
    path("", include("ProtocolosDigitales.urls")),
    path("", include("gestioncamas.urls", namespace="gestioncamas")),
    path("", include(("pacientes.urls", "pacientes"), namespace="pacientes")),
    path("", include(("users.urls", "users"), namespace="users")),
    path("", include("teleenfermeria.urls"), name="teleenfermeria"),
    path("", include("aislamientos.urls"), name="aislamientos"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
