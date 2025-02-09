from django import forms
from .models import Teleseguimiento, Seguimiento, Prescripcion, Turno, Medicacion
from users.models import User


class TeleseguimientoForm(forms.ModelForm):
    class Meta:
        model = Teleseguimiento
        fields = [
            "motivo_consulta",
            "condicion",
            "agente",
        ]
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
            "agente": forms.Select(
                attrs={"class": "form-control", "style": "width: 100%; border-radius: 5px;"}
            ),
        }

    def __init__(self, *args, **kwargs):
        paciente_id = kwargs.pop("paciente_id", None)
        super(TeleseguimientoForm, self).__init__(*args, **kwargs)

        # Set the paciente field as hidden and prefill if paciente_id is provided
        if paciente_id:
            self.fields["paciente"].initial = paciente_id
            self.fields["paciente"].widget = forms.HiddenInput()

        # Set the queryset for the agente field to all users
        if "agente" in self.fields:
            self.fields["agente"].queryset = User.objects.filter(groups__name="Teleenfermeria")

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


class MedicacionForm(forms.ModelForm):
    class Meta:
        model = Medicacion
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del medicamento'})
        }

class PrescripcionForm(forms.ModelForm):
    nueva_medicacion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Si no encuentra la medicación, ingrese el nombre aquí'
        })
    )
    class Meta:
        model = Prescripcion
        fields = ("medicacion", "tipo", "dosis", "via", "indicacion")
        widgets = {
            "medicacion": forms.Select(attrs={
                "class": "form-control",
                "data-toggle": "tooltip",
                "title": "Seleccione una medicación existente o ingrese una nueva abajo"
            }),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "dosis": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Dosis"}
            ),
            "via": forms.Select(attrs={"class": "form-control"}),
            "indicacion": forms.Select(attrs={"class": "form-control"}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medicacion'].required = False

    def clean(self):
        cleaned_data = super().clean()
        medicacion = cleaned_data.get('medicacion')
        nueva_medicacion = cleaned_data.get('nueva_medicacion')

        if not medicacion and not nueva_medicacion:
            raise forms.ValidationError(
                "Debe seleccionar una medicación existente o ingresar una nueva"
            )

        if nueva_medicacion:
            # Si hay una nueva medicación, ignoramos la selección del dropdown
            medicacion, created = Medicacion.objects.get_or_create(
                nombre=nueva_medicacion
            )
            cleaned_data['medicacion'] = medicacion
            return cleaned_data

        if not medicacion:
            raise forms.ValidationError(
                "Debe seleccionar una medicación existente si no ingresa una nueva"
            )

        return cleaned_data
=======

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
