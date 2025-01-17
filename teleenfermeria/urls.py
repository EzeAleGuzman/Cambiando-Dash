from django.urls import path
from . import views

urlpatterns = [
    path('crear_teleseguimiento/', views.crear_teleseguimiento, name='crear_teleseguimiento'),
    path('teleseguimiento/<int:pk>/', views.detalle_teleseguimiento, name='detalle_teleseguimiento'),
    path('teleseguimiento/<int:teleseguimiento_id>/crear_seguimiento/', views.crear_seguimiento, name='crear_seguimiento'),
]