# Generated by Django 5.1.4 on 2025-02-05 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0004_paciente_telefono2_alter_paciente_obra_social"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paciente",
            name="dni",
            field=models.CharField(
                blank=True, default="Sin DNI", max_length=15, null=True, unique=True
            ),
        ),
    ]
