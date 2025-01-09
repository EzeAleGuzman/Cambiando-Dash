from django import forms
from .models import PacienteCama
from pacientes.models import Paciente


class IngresarPacienteCamaForm(forms.ModelForm):
    dni_paciente = forms.CharField(label="DNI del Paciente", max_length=15)

    class Meta:
        model = PacienteCama
        fields = ['cama']

    def clean_dni_paciente(self):
        dni = self.cleaned_data.get('dni_paciente')
        try:
            paciente = Paciente.objects.get(dni=dni)
        except Paciente.DoesNotExist:
            raise forms.ValidationError("No se encontró ningún paciente con ese DNI.")
        return paciente
