from django.db import models

# Create your models here.
class Interno(models.Model):
    servicio = models.CharField(max_length=100)
    interno = models.CharField(max_length=100)