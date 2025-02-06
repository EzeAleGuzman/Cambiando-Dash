from django import forms
from .models import Teleseguimiento, Seguimiento, Prescripcion, Turno, User


class TeleseguimientoForm(forms.ModelForm):
    class Meta:
        model = Teleseguimiento
        fields = [
            "descripcion",
            "condicion",
            "diagnostico",
        ]  # Incluye solo los campos que deseas mostrar en el formulario
        widgets = {
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe la Motivo de solicitud...",
                    "style": "width: 50%; margin: 0 auto;",
                }
            ),
            "diagnostico": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "style": "width: 50%; margin: 0 auto;",
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
