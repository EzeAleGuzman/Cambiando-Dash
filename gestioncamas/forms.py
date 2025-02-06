# forms.py
from django import forms
from .models import Servicio, Ubicacion, Cama, PacienteCama

class AsignacionCamaForm(forms.ModelForm):
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.filter(activo=True),
        empty_label="Seleccione un servicio...",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'select-servicio'
        })
    )

    ubicacion = forms.ModelChoiceField(
        queryset=Ubicacion.objects.none(),
        empty_label="Seleccione una ubicación...",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'select-ubicacion'
        })
    )

    cama = forms.ModelChoiceField(
        queryset=Cama.objects.none(),
        empty_label="Seleccione una cama...",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'select-cama'
        })
    )

    class Meta:
        model = PacienteCama
        fields = ['servicio', 'ubicacion', 'cama']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'servicio' in self.data:
            try:
                servicio_id = int(self.data.get('servicio'))
                self.fields['ubicacion'].queryset = Ubicacion.objects.filter(
                    servicio_id=servicio_id,
                    activo=True
                )
            except (ValueError, TypeError):
                pass

        if 'ubicacion' in self.data:
            try:
                ubicacion_id = int(self.data.get('ubicacion'))
                self.fields['cama'].queryset = Cama.objects.filter(
                    ubicacion_id=ubicacion_id,
                    estado='LIBRE',
                    activo=True
                )
            except (ValueError, TypeError):
                pass


class LiberarCamaForm(forms.Form):
    motivo_liberacion = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={
            'class': 'form-control',  # Clase de Bootstrap para campos de formulario
            'rows': 4,  # Definir la altura del textarea
            'placeholder': 'Escribe el motivo de liberación...',  # Texto de ejemplo
        }),
        label="Motivo de liberación"
    )