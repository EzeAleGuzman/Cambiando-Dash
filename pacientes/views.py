from django.shortcuts import render
from .models import Paciente
from gestioncamas.models import Servicio
from django.shortcuts import get_object_or_404, redirect
from .forms import PacienteForm
from django.contrib.auth.decorators import login_required


@login_required
def Pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, "pacientes.html", {"pacientes": pacientes})


@login_required
def detallepaciente(request, id):
    paciente = Paciente.objects.get(pk=id)
    return render(request, "detallepaciente.html", {"paciente": paciente})


@login_required
def pacientesporservicio(request):
    servicio_seleccionado = request.GET.get("servicio", None)

    if servicio_seleccionado:
        # Filtrar pacientes por servicio y asegurarse de que tienen una cama asignada
        pacientes = (
            Paciente.objects.filter(
                pacientecama__cama__ubicacion__servicio_id=servicio_seleccionado,
                pacientecama__fecha_liberacion__isnull=True,  # Asegurarse de que tienen una cama asignada
            )
            .order_by("pacientecama__cama__ubicacion__nombre")
            .distinct()
        )
    else:
        # Si no se seleccionó servicio, no se muestran pacientes
        pacientes = []

    # Obtener todos los servicios para el filtro
    servicios = Servicio.objects.all()

    return render(
        request,
        "pacientesporservicio.html",
        {
            "pacientes": pacientes,
            "servicios": servicios,
            "servicio_seleccionado": servicio_seleccionado,
        },
    )


@login_required
def nuevopaciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            return redirect("pacientes:Pacientes")
    else:
        # Instanciar el formulario vacío

        form = PacienteForm()
        print(form.errors)
    return render(request, "nuevopaciente.html", {"form": form})


@login_required
def editarpaciente(request, id):
    # Obtener el paciente correspondiente
    paciente = get_object_or_404(Paciente, pk=id)

    if request.method == "POST":
        # Instanciar el formulario con los datos enviados por el usuario
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            # Si la petición es GET, instanciar el formulario con los datos del paciente
            # Verificar si la fecha de nacimiento es None

            # Guardar los cambios si el formulario es válido
            form.save()

            return redirect("pacientes:Pacientes")
        else:
            print("Formulario no válido")
            print(form.errors)

    else:
        if paciente.fecha_nacimiento:
            paciente.fecha_nacimiento = paciente.fecha_nacimiento.strftime("%Y-%m-%d")
        if paciente.fecha_ingreso:
            paciente.fecha_ingreso = paciente.fecha_ingreso.strftime("%Y-%m-%d")
        if paciente.fecha_egreso:
            paciente.fecha_egreso = paciente.fecha_egreso.strftime("%Y-%m-%d")
        else:
            paciente.fecha_egreso = ""
        if paciente.fecha_pase:
            paciente.fecha_pase = paciente.fecha_pase.strftime("%Y-%m-%d")
        else:
            paciente.fecha_pase = ""
        form = PacienteForm(instance=paciente)

    # Renderizar el template con el formulario
    return render(request, "editarpaciente.html", {"paciente": paciente, "form": form})
