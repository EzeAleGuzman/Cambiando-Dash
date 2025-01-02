from django.db import models
from pacientes.models import Paciente
from django.utils import timezone


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    color_identificativo = models.CharField(max_length=7)
    orden_visualizacion = models.IntegerField()
    capacidad_total = models.IntegerField()
    nivel_alerta_ocupacion = models.IntegerField()
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Ubicacion(models.Model):
    TIPO_CHOICES = [("HABITACION", "Habitación"), ("AREA", "Área")]
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(choices=TIPO_CHOICES, max_length=10)
    capacidad = models.IntegerField()
    notas = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Cama(models.Model):
    ESTADO_CHOICES = [
        ("LIBRE", "Libre"),
        ("OCUPADA", "Ocupada"),
        ("RESERVADA", "Reservada"),
        ("EN_REFACCION", "En Refacción"),
        ("FUERA_DE_SERVICIO", "Fuera de Servicio"),
    ]

    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)
    estado = models.CharField(choices=ESTADO_CHOICES, max_length=20)
    notas = models.TextField(blank=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    ultima_limpieza = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cama {self.numero}, Ubicación {self.ubicacion.nombre}, Servicio {self.ubicacion.servicio.nombre}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PacienteCama(models.Model):
     paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
     cama = models.ForeignKey(Cama, on_delete=models.CASCADE) 
     fecha_asignacion = models.DateTimeField(default=timezone.now) 
     fecha_liberacion = models.DateTimeField(null=True, blank=True) 
     def __str__(self): 
         return f"{self.paciente} - {self.cama}"