from django.urls import path
from . import views
from .views import Dashbord

urlpatterns = [
    path("dashboard/", views.Dashbord, name="dashboard"),
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
]
