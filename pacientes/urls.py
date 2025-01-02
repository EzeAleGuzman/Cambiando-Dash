from django.urls import path
from . import views

urlpatterns = [
    path('pacientes/', views.Pacientes, name='Pacientes'),
    path('pacientesporservicio/', views.pacientesporservicio, name='pacientes_por_servicio'),	
]