from django.db import models
from users.models import User
from pacientes.models import Paciente
from django.utils import timezone


class Medicacion(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


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
            ("pasivo", "Pasivo"),
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
    vacunas = models.CharField(
        max_length=28,
        choices=[
            ("completo", "Completo"),
            ("en_proceso", "En Proceso"),
            ("incompleto", "Incompleto"),   
        ],
        default="En proceso",
    )

    def __str__(self):
        return f"Teleseguimiento de {self.paciente.nombre_completo} - {self.fecha_solicitud.strftime('%Y-%m-%d %H:%M')}"

    def fecha_ultimo_seguimiento(self):
        ultimo_seguimiento = self.seguimiento_set.order_by("-fecha").first()
        return ultimo_seguimiento.fecha if ultimo_seguimiento else None


class Prescripcion(models.Model):
    teleseguimiento = models.ForeignKey(
        Teleseguimiento, on_delete=models.CASCADE, related_name="prescripciones"
    )
    medicacion = models.ForeignKey(Medicacion, on_delete=models.CASCADE)
    dosis = models.CharField(max_length=50)
    via = models.CharField(
        max_length=50,
        choices=[
            ("oral", "Oral"),
            ("puff", "Puff"),
            ("endovenosa", "Endovenosa"),
            ("intramuscular", "Intramuscular"),
            ("subcutanea", "Subcutánea"),
            ("otro", "Otro"),
        ],
        default="oral",
    )
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("antibiotico", "Antibiótico"),
            ("antipiretico", "Antipirético"),
            ("analgesico", "Analgésico"),
            ("antiinflamatorio", "Antiinflamatorio"),
            ("aerosol", "Aerosol"),
            ("corticosteroide", "Corticosteroide"),
        ],
        default="otro",
    )
    indicacion = models.CharField(
        max_length=50,
        choices=[
            ("6h", "Cada 6 horas"),
            ("8h", "Cada 8 horas"),
            ("12h", "Cada 12 horas"),
            ("24h", "Cada 24 horas"),
        ],
    )

    def __str__(self):
        return f"{self.medicacion.nombre} - {self.dosis} ({self.via}) para {self.teleseguimiento.paciente.nombre_completo}"


class Seguimiento(models.Model):
    id = models.AutoField(primary_key=True)
    teleseguimiento = models.ForeignKey(Teleseguimiento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Asignar directamente del usuario logueado
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(max_length=1000)

    def __str__(self):
        return f"Seguimiento de {self.teleseguimiento.paciente.nombre_completo} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"


class SolicitudTurno(models.Model):
    teleseguimiento = models.ForeignKey(Teleseguimiento, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "Pendiente"),
            ("confirmado", "Confirmado"),
            ("cancelado", "Cancelado"),
        ],
        default="pendiente",
    )
    especialidad = models.CharField(
        max_length=50,
        choices=[
            ("Otorrinolaringología", "Otorrinolaringología"),
            ("cardiologia", "Cardiología"),
            ("dermatologia", "Dermatología"),
            ("neurologia", "Neurología"),
            ("pediatria", "Pediatría"),
            ("psiquiatria", "Psiquiatría"),
            ("traumatologia", "Traumatología"),
            ("urologia", "Urología"),
            ("ginecologia", "Ginecología"),
            ("oftalmologia", "Oftalmología"),
        ],
    )

    def __str__(self):
        return f"Solicitud de turno para {self.teleseguimiento.paciente.nombre_completo} - {self.fecha_solicitud.strftime('%Y-%m-%d %H:%M')} - {self.especialidad}"


class Turno(models.Model):
    solicitud_turno = models.ForeignKey(SolicitudTurno, on_delete=models.CASCADE)
    fecha_turno = models.DateTimeField()
    hora_turno = models.TimeField()
    profesional = models.CharField(max_length=50)

    def __str__(self):
        return f"Turno de {self.solicitud_turno.teleseguimiento.paciente.nombre_completo} - {self.fecha_turno.strftime('%Y-%m-%d %H:%M')}"
