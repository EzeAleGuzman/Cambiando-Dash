from django.urls import path
from . import views

urlpatterns = [
    path('pacientes/', views.Pacientes, name='Pacientes'),
    path('pacientesporservicio/', views.pacientesporservicio, name='pacientes_por_servicio'),
    path('nuevopaciente/', views.nuevopaciente, name='nuevopaciente'),
    path('detallepaciente/<int:id>/', views.detallepaciente, name='detallepaciente'),
    path('editarpaciente/<int:id>/', views.editarpaciente, name='editarpaciente'),
    path('registropaciente/', views.nuevopaciente, name='nuevopaciente'),
]