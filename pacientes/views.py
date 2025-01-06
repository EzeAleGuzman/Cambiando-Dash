from django.shortcuts import render
from .models import Paciente
from gestioncamas.models import Servicio
from django.shortcuts import get_object_or_404, redirect
from .forms import PacienteForm

# Create your views here.
def Pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes.html', {'pacientes': pacientes})

def detallepaciente(request,id):
    paciente = Paciente.objects.get(pk=id)
    return render(request, 'detallepaciente.html', {'paciente': paciente})

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




def editarpaciente(request, id):
    # Obtener el paciente correspondiente
    paciente = get_object_or_404(Paciente, pk=id)

    if request.method == 'POST':
        # Instanciar el formulario con los datos enviados por el usuario
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
             # Si la petición es GET, instanciar el formulario con los datos del paciente
        # Verificar si la fecha de nacimiento es None
            
            # Guardar los cambios si el formulario es válido
            form.save()

            return redirect('Pacientes')
        else:
            print("Formulario no válido")
            print(form.errors)

       
    else: 
        if paciente.fecha_nacimiento:
            paciente.fecha_nacimiento = paciente.fecha_nacimiento.strftime('%Y-%m-%d')
        if paciente.fecha_ingreso:
            paciente.fecha_ingreso = paciente.fecha_ingreso.strftime('%Y-%m-%d')
        if paciente.fecha_egreso:
            paciente.fecha_egreso = paciente.fecha_egreso.strftime('%Y-%m-%d')
        else:
            paciente.fecha_egreso = ""
        if paciente.fecha_pase:
            paciente.fecha_pase = paciente.fecha_pase.strftime('%Y-%m-%d')   
        else:
            paciente.fecha_pase = ""
        form = PacienteForm(instance=paciente)

    # Renderizar el template con el formulario
    return render(request, 'editarpaciente.html', {'paciente': paciente, 'form': form})