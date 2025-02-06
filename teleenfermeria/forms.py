from django import forms
from .models import Teleseguimiento, Seguimiento, Prescripcion, Turno, User


class TeleseguimientoForm(forms.ModelForm):
    class Meta:
        model = Teleseguimiento
        fields = [
            "motivo_consulta",
            "condicion",
        ]  # Incluye solo los campos que deseas mostrar en el formulario
        widgets = {
            "motivo_consulta": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe el motivo de consulta...",
                    "style": "width: 100%; margin: 0 auto; border-radius: 5px; padding: 10px;",
                }
            ),
            "condicion": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Seleccione condición",
                    "style": "width: 100%; margin: 0 auto; border-radius: 5px; padding: 10px;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        paciente_id = kwargs.pop("paciente_id", None)
        super(TeleseguimientoForm, self).__init__(*args, **kwargs)
        if paciente_id:
            self.fields["paciente"].initial = paciente_id
            self.fields["paciente"].widget = forms.HiddenInput()


class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = Seguimiento
        fields = ["descripcion"]
        widgets = {
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe el seguimiento...",
                }
            ),
        }


class PrescripcionForm(forms.ModelForm):

    class Meta:
        model = Prescripcion
        fields = ("medicacion", "tipo", "dosis", "via", "indicacion")
        widgets = {
            "medicacion": forms.Select(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "dosis": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Dosis"}
            ),
            "via": forms.Select(attrs={"class": "form-control"}),
            "indicacion": forms.Select(attrs={"class": "form-control"}),
        }


class AsignarTurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ["fecha_turno", "hora_turno", "profesional"]
        widgets = {
            "fecha_turno": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "hora_turno": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "profesional": forms.TextInput(attrs={"class": "form-control"}),
        }


class FiltrarTeleseguimientoForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=User.objects.none(), required=False, label="Usuario"
    )

    def __init__(self, *args, **kwargs):
        usuarios = kwargs.pop("usuarios", None)
        super(FiltrarTeleseguimientoForm, self).__init__(*args, **kwargs)
        if usuarios is not None:

            self.fields["usuario"].queryset = usuarios


class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Teleseguimiento
        fields = ["diagnostico"]
        widgets = {
            "diagnostico": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Ingrese el diagnóstico...",
                    "style": "width: 100%; margin: 0 auto; border-radius: 5px; padding: 10px;",
                }
            ),
        }
