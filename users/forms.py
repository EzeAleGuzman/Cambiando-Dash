from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "name", "lastname", "cellphone", "servicio", "cargo", "password1", "password2")
        error_messages = {
            'email': {
                'unique': "Ya existe un/a Usuario con este/a Email.",
            },
            'password_mismatch': "Las contraseñas no coinciden.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = 'Correo Electrónico'
        self.fields["name"].label = 'Nombre'
        self.fields["lastname"].label = 'Apellido'
        self.fields["cellphone"].label = 'Celular'
        self.fields["servicio"].label = 'Servicio'
        self.fields["cargo"].label = 'Cargo'
        self.fields["password1"].label = 'Contraseña'
        self.fields["password2"].label = 'Confirmar Contraseña'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        self.fields['password1'].error_messages.update({
            'required': 'Este campo es obligatorio.',
            'password_too_similar': 'Su contraseña no puede ser similar a otros componentes de su información personal.',
            'password_too_short': 'Su contraseña debe contener por lo menos 8 caracteres.',
            'password_common': 'Su contraseña no puede ser una contraseña usada muy comúnmente.',
            'password_entirely_numeric': 'Su contraseña no puede estar formada exclusivamente por números.',
        })

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "name", "lastname", "cellphone", "servicio", "cargo", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label



class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Correo Electrónico', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))