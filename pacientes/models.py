from django.db import models
from django.utils import timezone

class Paciente(models.Model):
    # Datos personales
    nombre_completo = models.CharField(max_length=255, null=True, blank=True)
    dni = models.CharField(max_length=15, unique=True)
    fecha_nacimiento = models.DateField()
    domicilio = models.CharField(max_length=255, null=True, blank=True)
    localidad = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20)
    obra_social = models.CharField(max_length=100, null=True, blank=True)

    # Información de internación
    fecha_ingreso = models.DateField(default=timezone.now)
    diagnostico = models.CharField(max_length=255, null=True, blank=True)
    causa_externa = models.CharField(max_length=255, null=True, blank=True)  # Solo para pediatría/guardia
    arm = models.BooleanField(default=False)  # Si necesita asistencia respiratoria
    tipo_egreso = models.CharField(max_length=50, null=True, blank=True)  # Alta, Derivado, etc.
    fecha_egreso = models.DateField(null=True, blank=True)

    # Información para pediatría
    nombre_tutor = models.CharField(max_length=255, null=True, blank=True)
    dni_tutor = models.CharField(max_length=15, null=True, blank=True)

    # Historia clínica y pases entre servicios
    historia_clinica = models.CharField(max_length=50, null=True, blank=True)
    pases = models.CharField(max_length=255, null=True, blank=True)  # Detalle de los pases
    fecha_pase = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_completo} ({self.dni})"

    @property
    def cama_actual(self):
        paciente_cama = self.pacientecama_set.filter(fecha_liberacion__isnull=True).first()
        return paciente_cama.cama if paciente_cama else None

    def obtener_info_cama(self):
        cama = self.cama_actual
        if cama:
            return {
                "servicio": cama.ubicacion.servicio.nombre,
                "ubicacion": cama.ubicacion.nombre,
                "numero": cama.numero
            }
        else:
            return {
                "servicio": "N/A",
                "ubicacion": "N/A",
                "numero": "No tiene cama asignada"
            }
