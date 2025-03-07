from django.urls import path
from . import views

app_name = 'aislamientos'

urlpatterns = [
    path("crearaislamiento/<int:paciente_id>/",
    views.crearaislamiento,
    name='crearaislamiento'),
    path("finalizaraislamiento/<int:aislamiento_id>/",
    views.finalizaraislamiento,
    name='finalizaraislamiento'),
]