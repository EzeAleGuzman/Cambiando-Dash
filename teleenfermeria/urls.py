from django.urls import path
from . import views

app_name = "teleenfermeria"

urlpatterns = [
    path(
        "crear_teleseguimiento/<int:paciente_id>/",
        views.solicitarteleseguimiento,
        name="crear_teleseguimiento",
    ),
    path("derivados/", views.derivadosteleseguimiento, name="derivados"),
    path(
        "detalle/<int:teleseguimiento_id>/",
        views.detalleteleseguimiento,
        name="detalleteleseguimiento",
    ),
    path(
        "crear_seguimiento/<int:teleseguimiento_id>/",
        views.crearseguimiento,
        name="crear_seguimiento",
    ),
    path(
        "modificar_consentimiento/<int:teleseguimiento_id>/<str:nuevo_estado>/",
        views.modificar_consentimiento,
        name="modificar_consentimiento",
    ),
    path(
        "en_proceso/",
        views.enprocesoteleseguimiento,
        name="en_proceso",
    ),
    path(
        "rechazados/",
        views.telezeguimientosrechazados,
        name="rechazados",
    ),
    path(
        "crear_prescripcion/<int:teleseguimiento_id>/",
        views.agregar_prescripcion,
        name="crear_prescripcion",
    ),
    path(
        "solicitar_turno/<int:teleseguimiento_id>/",
        views.solicitarturno,
        name="solicitar_turno",
        ),
]
