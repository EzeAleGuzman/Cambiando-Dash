from django.shortcuts import render
from .models import Paciente
from gestioncamas.models import Servicio

# Create your views here.
def Pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes.html', {'pacientes': pacientes})

def pacientesporservicio(request):
    servicio_seleccionado = request.GET.get('servicio', None)
    
    if servicio_seleccionado:
        # Si se seleccionó un servicio, se filtran los pacientes de ese servicio
        pacientes = Paciente.objects.filter(pacientecama__cama__ubicacion__servicio_id=servicio_seleccionado)
    else:
        # Si no se seleccionó servicio, no se muestran pacientes
        pacientes = []

    # Obtener todos los servicios para el filtro
    servicios = Servicio.objects.all()

    return render(
        request,
        'pacientesporservicio.html',  # Cambia esto por el nombre de tu template real
        {
            'pacientes': pacientes,
            'servicios': servicios,
            'servicio_seleccionado': servicio_seleccionado
        }
    )