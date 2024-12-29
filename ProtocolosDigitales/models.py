from django.db import models
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Documento(models.Model):
    Opciones_clases = [
        ("Normativa General", "Normativa General"),
        ("Protocolo de Control de Infecciones", "Protocolo de Control de Infecciones"),
        ("Protocolos Generales", "Protocolos Generales"),
        ("Protocolos de Servicio", "Protocolos de Servicio"),
        ("Instructivo de Procedimiento", "Instructivo de Procedimiento"),
    ]
    clase = models.CharField(
        max_length=50, choices=Opciones_clases, blank=False, null=False
    )
    nombre = models.CharField(max_length=100, unique=True, blank=False, null=False)
    codigo = models.CharField(max_length=50, unique=True, blank=False, null=False)

    def __str__(self):
        return self.nombre


class VersionDocumento(models.Model):
    documento = models.ForeignKey(
        Documento, on_delete=models.CASCADE, related_name="versiones"
    )
    version = models.PositiveBigIntegerField()
    archivo_pdf = models.FileField(upload_to="documentos/")
    fecha_creacion = models.DateTimeField(null=False, blank=False)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    fecha_implementacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.documento.nombre} - Version: {self.version}, archivo: {self.archivo_pdf}"


@receiver(pre_save, sender=VersionDocumento)
def actualizar_version(sender, instance, **kwargs):
    if instance.pk is None:
        ultima_version = (
            VersionDocumento.objects.filter(documento=instance.documento)
            .order_by("-version")
            .first()
        )
        instance.version = 1 if ultima_version is None else ultima_version.version + 1
