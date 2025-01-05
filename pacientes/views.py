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
    
def nuevopaciente(request):
    if request.method == 'POST':
        # Crear un nuevo paciente
        dni = request.POST.get('dni', None)
        nombre = request.POST.get('nombre', None)
        apellido = request.POST.get('apellido', None)
        fecha_nacimiento = request.POST.get('fecha_nacimiento', None)
        sexo = request.POST.get('sexo', None)
        direccion = request.POST.get('direccion', None)
        telefono = request.POST.get('telefono', None)
        email = request.POST.get('email', None)
        
        paciente = Paciente(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            direccion=direccion,
            telefono=telefono,
            email=email
        )
        paciente.save()
        return render(request, 'nuevopaciente.html', {'paciente': paciente})
    else:
        return render(request, 'nuevopaciente.html', {'paciente': None})


def eliminarpaciente(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    paciente.delete()
    return render(request, 'eliminarpaciente.html', {'paciente': paciente}) 