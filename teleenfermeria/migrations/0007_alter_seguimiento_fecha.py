# Generated by Django 5.1.4 on 2025-01-27 12:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teleenfermeria', '0006_remove_medicacion_tipo_remove_medicacion_via_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seguimiento',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
