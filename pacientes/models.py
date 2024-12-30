from django.db import models





class Paciente(models.Model):
    GÉNERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'No especificado'),
        ('P', 'Prefiero no decirlo'),
    ]
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)
    fecha_nacimiento = models.Dasexo = models.CharField(max_length=100)
    genero = models.CharField(max_length=1, choices=GÉNERO_CHOICES)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'	

class Registro(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    registro = models.TextField()

    def __str__(self):
        return f'{self.paciente.nombre} {self.paciente.apellido}'