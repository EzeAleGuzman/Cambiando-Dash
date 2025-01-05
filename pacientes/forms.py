from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['dni', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo', 'direccion', 'telefono', 'email']
        labels = {
            'dni': 'DNI',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'sexo': 'Sexo',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Email'
        }
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }
        help_texts = {
            'dni': 'DNI del paciente',
            'nombre': 'Nombre del paciente',
            'apellido': 'Apellido del paciente',
            'fecha_nacimiento': 'Fecha de nacimiento del paciente',
            'sexo': 'Sexo del paciente',
            'direccion': 'Dirección del paciente',
            'telefono': 'Teléfono del paciente',
            'email': 'Email del paciente'
        }