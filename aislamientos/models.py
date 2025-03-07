from django.db import models
from gestioncamas.models import PacienteCama

# Create your models here.
class TipoAislamiento(models.Model):
    nombre = models.CharField(max_length=50, choices=[('Contacto', 'Contacto'), ('Respiratorio', 'Respiratorio'), ('Gotas', 'Gotas'), ('Aéreo', 'Aéreo')], default='Contacto')
    color = models.CharField(max_length=50)
    imagen_ilustracion = models.ImageField(upload_to='aislamientos/imagenes', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Aislamiento(models.Model):
    tipo = models.ForeignKey(TipoAislamiento, on_delete=models.CASCADE)
    cama_paciente = models.ForeignKey(PacienteCama, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
  

    def __str__(self):
        return self.tipo.nombre + ' ' + self.fecha_inicio.strftime('%d/%m/%Y')
    
