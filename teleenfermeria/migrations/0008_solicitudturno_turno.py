# Generated by Django 5.1.4 on 2025-01-27 23:27

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teleenfermeria', '0007_alter_seguimiento_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudTurno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_solicitud', models.DateTimeField(default=django.utils.timezone.now)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('confirmado', 'Confirmado'), ('cancelado', 'Cancelado')], default='pendiente', max_length=20)),
                ('especialidad', models.CharField(choices=[('Otorrinolaringología', 'Otorrinolaringología'), ('cardiologia', 'Cardiología'), ('dermatologia', 'Dermatología'), ('neurologia', 'Neurología'), ('pediatria', 'Pediatría'), ('psiquiatria', 'Psiquiatría'), ('traumatologia', 'Traumatología'), ('urologia', 'Urología'), ('ginecologia', 'Ginecología'), ('oftalmologia', 'Oftalmología')], max_length=50)),
                ('teleseguimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teleenfermeria.teleseguimiento')),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_turno', models.DateTimeField()),
                ('hora_turno', models.TimeField()),
                ('profesional', models.CharField(max_length=50)),
                ('solicitud_turno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teleenfermeria.solicitudturno')),
            ],
        ),
    ]
