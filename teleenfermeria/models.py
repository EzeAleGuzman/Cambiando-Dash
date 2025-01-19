from django.db import models
from users.models import User
from pacientes.models import Paciente


class Medicacion(models.Model):
    nombre = models.CharField(max_length=100)
    via = models.CharField(
        choices=[
            ('Oral', 'Oral'),
            ('Puff', 'Puff'),
            ('Endovenosa', 'Endovenosa'),
            ('Intramuscular', 'Intramuscular'),
            ('Subcutanea', 'Subcutanea'),
            ('Otro', 'Otro')
        ],
        default='Oral')
    dosis = models.CharField(max_length=100)
    indicacion = models.CharField(
        choise=[
            ('Cada 6 horas', 'Cada 6 horas'),
            ('Cada 8 horas', 'Cada 8 horas'),
            ('Cada 12 horas', 'Cada 12 horas'),
            ('Cada 24 horas', 'Cada 24 horas')
        ],
        )


class Teleseguimiento(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=1000, blank=True, null=True)
    condicion = models.CharField(max_length=100, 
                                 choices=[
                                     (" Alta Medica"," Alta Medica"),
                                     ("Internado","Internado"),
                                     ("Otro","Otro")],
                                       default="Alta Medica")
    consentimiento_seguimiento = models.BooleanField(
        choices=[
            (True, 'Aceptado'),
              (False, 'Rechazado')],
                default=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('Derivado', 'Derivado'),
            ('en_proceso', 'En Proceso'),
            ('realizado', 'Realizado'),
            ('no_realizado', 'No Realizado')
        ],
        default='Derivado'
    )
    diagnostico = models.TextField(max_length=1000, blank=True, null=True)
    medicaciones = models.ManyToManyField(Medicacion, blank=True)
    
    def __str__(self):
        return f"Teleseguimiento de {self.paciente.nombre} - {self.fecha_solicitud.strftime('%Y-%m-%d %H:%M')}"

class Seguimiento(models.Model):
    id = models.AutoField(primary_key=True)
    teleseguimiento = models.ForeignKey(Teleseguimiento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Asignar directamente del usuario logueado
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=1000)
    estado = models.BooleanField(default=False)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('Derivado', 'Derivado'),
            ('realizado', 'Realizado'),
            ('no_realizado', 'No Realizado')
        ],
        default='en_proceso'
    )

    def __str__(self):
        return f"Seguimiento de {self.teleseguimiento.paciente.nombre} - {self.fecha.strftime('%Y-%m-%d %H:%M') - {self.estado}}"