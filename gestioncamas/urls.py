from django.urls import path
from . import views

app_name = "gestioncamas"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("obtener_ocupacion/", views.obtener_ocupacion, name="obtener_ocupacion"),
    path(
        "habitaciones-por-servicio/",
        views.habitaciones_por_servicio,
        name="habitaciones_por_servicio",
    ),
    path(
        "ubicacion/<int:ubicacion_id>/",
        views.ubicacion_detalle,
        name="ubicacion_detalle",
    ),
    path("asignar-cama/<int:paciente_id>/", views.asignar_cama, name="asignar_cama"),
    path("liberar-cama/<int:paciente_id>/", views.liberar_cama, name="liberar_cama"),
]
