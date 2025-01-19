from django import forms
from .models import Teleseguimiento, Seguimiento

class TeleseguimientoForm(forms.ModelForm):
    class Meta:
        model = Teleseguimiento
        fields = ['paciente', 'descripcion', 'condicion', 'estado']

class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = Seguimiento
        fields = ['descripcion', 'estado']