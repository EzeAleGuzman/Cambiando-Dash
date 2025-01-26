from django.db import models
from users.models import User
from pacientes.models import Paciente
from django.utils import timezone


class Medicacion(models.Model):
    nombre = models.CharField(max_length=50)
    via = models.CharField(
        choices=[
            ("Oral", "Oral"),
            ("Puff", "Puff"),
            ("Endovenosa", "Endovenosa"),
            ("Intramuscular", "Intramuscular"),
            ("Subcutanea", "Subcutanea"),
            ("Otro", "Otro"),
        ],
        default="Oral",
        max_length=50,
    )
    dosis = models.CharField(max_length=50)
    indicacion = models.CharField(
        choices=[
            ("Cada 6 horas", "Cada 6 horas"),
            ("Cada 8 horas", "Cada 8 horas"),
            ("Cada 12 horas", "Cada 12 horas"),
            ("Cada 24 horas", "Cada 24 horas"),
        ],
        max_length=50,
    )


class Teleseguimiento(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(max_length=1000, blank=True, null=True)
    condicion = models.CharField(
        max_length=100,
        choices=[
            (" Alta Medica", " Alta Medica"),
            ("Internado", "Internado"),
            ("Otro", "Otro"),
        ],
        default="Alta Medica",
    )
    consentimiento_seguimiento = models.CharField(
        max_length=100,
        choices=[
            ("aceptado", "Aceptado"),
            ("Rechazado", "Rechazado"),
            ("En espera", "En espera"),
        ],
        default="en_espera",
    )
    estado = models.CharField(
        max_length=20,
        choices=[
            ("Derivado", "Derivado"),
            ("en_proceso", "En Proceso"),
            ("realizado", "Realizado"),
            ("no_realizado", "No Realizado"),
        ],
        default="Derivado",
    )
    diagnostico = models.TextField(max_length=1000, blank=True, null=True)
    medicaciones = models.ManyToManyField(Medicacion, blank=True)

    def __str__(self):
        return f"Teleseguimiento de {self.paciente.nombre_completo} - {self.fecha_solicitud.strftime('%Y-%m-%d %H:%M')}"


class Seguimiento(models.Model):
    id = models.AutoField(primary_key=True)
    teleseguimiento = models.ForeignKey(Teleseguimiento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Asignar directamente del usuario logueado
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=1000)

    def __str__(self):
        return f"Seguimiento de {self.teleseguimiento.paciente.nombre_completo} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
