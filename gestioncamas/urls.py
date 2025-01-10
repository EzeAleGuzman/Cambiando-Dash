from django.urls import path
from . import views
from .views import Dashbord

app_name = 'gestioncamas'

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
    path('asignar-cama/<int:paciente_id>/', views.asignar_cama, name='asignar_cama'),
   
]
