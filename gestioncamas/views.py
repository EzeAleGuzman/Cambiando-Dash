from .models import Cama, Servicio, Ubicacion, PacienteCama
from django.shortcuts import render, get_object_or_404
from pacientes.models import Paciente
from .forms import AsignacionCamaForm, LiberarCamaForm
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    total_pacientes = Paciente.objects.count()
    camas_ocupadas = Cama.objects.filter(estado='OCUPADA').count()
    camas_libres = Cama.objects.filter(estado='LIBRE').count()
    total_camas_funcionales = camas_ocupadas + camas_libres  # Total de camas funcionales es la suma de camas ocupadas y libres
    pacientes_internados = PacienteCama.objects.filter(fecha_liberacion__isnull=True).count()  # Pacientes con cama asignada y fecha de egreso null
    print(camas_ocupadas)
    context = {
        'total_pacientes': total_pacientes,
        'camas_ocupadas': camas_ocupadas,
        'camas_libres': camas_libres,
        'total_camas_funcionales': total_camas_funcionales,
        'pacientes_internados': pacientes_internados,
    }
    return render(request, 'gestioncamas/dashboard.html', context)


def obtener_ocupacion(request):
    servicios = Servicio.objects.all()
    ocupacion_data = []

    for servicio in servicios:
        camas_totales = Cama.objects.filter(ubicacion__servicio=servicio).count()
        camas_ocupadas = PacienteCama.objects.filter(
            cama__ubicacion__servicio=servicio, fecha_liberacion__isnull=True
        ).count()
        camas_libres = camas_totales - camas_ocupadas
        ocupacion_data.append(
            {
                "servicio": servicio.nombre,
                "ocupadas": camas_ocupadas,
                "libres": camas_libres,
            }
        )

    return JsonResponse({"ocupacion_data": ocupacion_data})


@login_required
def habitaciones_por_servicio(request):
    servicios = Servicio.objects.all()
    data = []

    for servicio in servicios:
        ubicaciones = (
            servicio.ubicacion_set.all()
        )  # Obtener todas las ubicaciones asociadas al servicio
        for ubicacion in ubicaciones:
            camas = ubicacion.cama_set.all()  # Obtener todas las camas de la ubicación
            total_camas = camas.count()
            camas_libres = camas.filter(estado="LIBRE").count()
            camas_ocupadas = total_camas - camas_libres

            # Determina el color de la ubicación: verde si hay camas libres, rojo si no
            if camas_libres > 0:
                color = "green"  # Hay camas libres
            else:
                color = "red"  # Todas las camas están ocupadas

            # Agregar la información de la ubicación y camas a la lista de datos
            data.append(
                {
                    "servicio": servicio,
                    "ubicacion": ubicacion,
                    "total_camas": total_camas,
                    "camas_libres": camas_libres,
                    "camas_ocupadas": camas_ocupadas,
                    "color": color,
                }
            )

    return render(
        request,
        "gestioncamas/habitaciones_por_servicio.html",
        {"data": data, "servicios": servicios},
    )


def ubicacion_detalle(request, ubicacion_id):
    # Obtener la ubicación seleccionada
    ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id)

    # Obtener las camas asociadas a esa ubicación
    camas = Cama.objects.filter(ubicacion=ubicacion)

    # Filtrar pacientes asignados
    camas_con_paciente = PacienteCama.objects.filter(
        cama__in=camas, paciente__isnull=False
    )
    camas_libres = camas.filter(pacientecama__isnull=True)

    context = {
        "ubicacion": ubicacion,
        "camas_con_paciente": camas_con_paciente,
        "camas_libres": camas_libres,
    }

    return render(request, "gestioncamas/ubicacion_detalle.html", context)


@login_required
def asignar_cama(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Verificar si el paciente ya tiene una cama asignada
    if paciente.cama_actual:
        messages.warning(request, "El paciente ya tiene una cama asignada")
        return redirect("pacientes:detallepaciente", id=paciente_id)

    if request.method == "POST":
        form = AsignacionCamaForm(request.POST)
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.paciente = paciente
            asignacion.save()

            messages.success(
                request, f"Cama {asignacion.cama.numero} asignada exitosamente"
            )
            return redirect("pacientes:detallepaciente", id=paciente_id)
    else:
        form = AsignacionCamaForm()

    return render(
        request,
        "gestioncamas/asignar_cama.html",
        {
            "form": form,
            "paciente": paciente,
        },
    )


@login_required
def liberar_cama(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    asignacion_actual = paciente.pacientecama_set.filter(
        fecha_liberacion__isnull=True
    ).first()

    if not asignacion_actual:
        messages.warning(request, "El paciente no tiene una cama asignada actualmente")
        return redirect("pacientes:detallepaciente", id=paciente_id)

    if request.method == "POST":
        form = LiberarCamaForm(request.POST)
        if form.is_valid():
            # Actualizar la asignación
            asignacion_actual.fecha_liberacion = timezone.now()
            asignacion_actual.save()

            # Registrar el motivo y observaciones
            cama = asignacion_actual.cama
            cama.notas = (
                f"Liberada el {timezone.now().strftime('%d/%m/%Y %H:%M')}. "
                f"Motivo: {form.cleaned_data['motivo_liberacion']}. "
                f"Observaciones: {form.cleaned_data['observaciones']}"
            )
            cama.estado = "LIBRE"
            cama.save()

            messages.success(request, "Cama liberada exitosamente")
            return redirect("pacientes:detallepaciente", id=paciente_id)
    else:
        form = LiberarCamaForm()

    return render(
        request,
        "gestioncamas/liberar_cama.html",
        {"form": form, "paciente": paciente, "asignacion": asignacion_actual},
    )
