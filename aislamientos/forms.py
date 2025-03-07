from django import forms
from .models import Aislamiento

class AislamientoForm(forms.ModelForm):
    class Meta:
        model = Aislamiento
        fields = ['tipo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Seleccione el Tipo de aislamiento'})

