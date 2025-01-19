from django.contrib import admin
from .models import Teleseguimiento, Seguimiento

app_name = 'teleenfermeria'

admin.site.register(Teleseguimiento)
admin.site.register(Seguimiento)