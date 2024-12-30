from django.urls import path
from . import views
from .views import DashboardView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('habitaciones-por-servicio/', views.habitaciones_por_servicio, name='habitaciones_por_servicio'),
]