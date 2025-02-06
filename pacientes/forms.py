from django import forms
from .models import Paciente
from django.forms import DateInput

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nombre_completo', 'dni', 'fecha_nacimiento', 'domicilio',
            'localidad', 'telefono', 'obra_social', 'fecha_ingreso',
            'diagnostico', 'causa_externa', 'arm', 'tipo_egreso',
            'fecha_egreso', 'nombre_tutor', 'dni_tutor', 'historia_clinica',
            'pases', 'fecha_pase'
        ]

    # Campos de fecha
    fecha_nacimiento = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    fecha_ingreso = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    fecha_egreso = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    fecha_pase = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )

    # Campos de texto
    nombre_completo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255
    )
    dni = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=20,
        required=False
    )

    domicilio = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255,
        required=False
    )
    localidad = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False
    )
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=20
    )
    obra_social = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False
    )
    diagnostico = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    causa_externa = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    arm = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-control'}),
        required=False
        )

    tipo_egreso = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False
    )
    nombre_tutor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255,
        required=False
    )
    dni_tutor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=20,
        required=False
    )
    historia_clinica = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    pases = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni:  # Si el DNI está vacío
            return None  # Lo tratamos como NULL
        return dni

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Asegurarse de que las fechas ya guardadas se muestren correctamente en el formulario
        if self.instance and self.instance.fecha_nacimiento:
            self.fields['fecha_nacimiento'].initial = self.instance.fecha_nacimiento
        if self.instance and self.instance.fecha_ingreso:
            self.fields['fecha_ingreso'].initial = self.instance.fecha_ingreso
        if self.instance and self.instance.fecha_egreso:
            self.fields['fecha_egreso'].initial = self.instance.fecha_egreso
        if self.instance and self.instance.fecha_pase:
            self.fields['fecha_pase'].initial = self.instance.fecha_pase


