from django.shortcuts import render
from .models import Paciente
from gestioncamas.models import Servicio
from django.shortcuts import get_object_or_404, redirect
from .forms import PacienteForm
from django.contrib.auth.decorators import login_required
from teleenfermeria.views import (
    group_required,

)


@login_required
def Pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, "pacientes.html", {"pacientes": pacientes})


@login_required
def detallepaciente(request, id):
    paciente = Paciente.objects.get(pk=id)
    return render(request, "detallepaciente.html", {"paciente": paciente})


@login_required
@group_required("Administrativo")
def pacientesporservicio(request):
    servicio_seleccionado_id = request.GET.get("servicio", None)
    servicio_seleccionado = None

    if servicio_seleccionado_id:
        servicio_seleccionado = get_object_or_404(Servicio, id=servicio_seleccionado_id)
        # Filtrar pacientes por servicio y asegurarse de que tienen una cama asignada
        pacientes = (
            Paciente.objects.filter(
                pacientecama__cama__ubicacion__servicio=servicio_seleccionado,
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
            paciente = form.save(commit=False)
            if not paciente.dni:  # Si no se ha proporcionado un DNI
                paciente.dni = None  # Guardar como NULL en lugar de una cadena vacía
            paciente.save()
            return redirect("pacientes:Pacientes")
        else:
            # Imprimir los errores en la consola (para depuración)
            print(form.errors)
            # Renderizar la misma plantilla mostrando los errores del formulario
            return render(request, "nuevopaciente.html", {"form": form})
    else:
        form = PacienteForm()
    return render(request, "nuevopaciente.html", {"form": form})


@login_required
@group_required("Administrativo")
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
