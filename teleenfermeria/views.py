from django.shortcuts import render, redirect, get_object_or_404
from pacientes.models import Paciente
from .models import Teleseguimiento, Seguimiento
from .forms import TeleseguimientoForm, SeguimientoForm


def solicitarteleseguimiento(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == "POST":
        form = TeleseguimientoForm(request.POST)
        if form.is_valid():
            teleseguimiento = form.save(commit=False)
            teleseguimiento.paciente = paciente
            teleseguimiento.save()
            # Redirigir a la vista de detalle del paciente
            return redirect("pacientes:detallepaciente", id=paciente_id)
    else:
        form = TeleseguimientoForm()
    return render(
        request,
        "teleenfermeria/crear_teleseguimiento.html",
        {"form": form, "paciente": paciente},
    )


def derivadosteleseguimiento(request):
    teleseguimientos = Teleseguimiento.objects.filter(estado="Derivado")
    return render(
        request,
        "teleenfermeria/derivados_teleseguimiento.html",
        {"teleseguimientos": teleseguimientos},
    )

def enprocesoteleseguimiento(request):
    teleseguimientos = Teleseguimiento.objects.filter(estado="en_proceso")
    return render(
        request,
        "teleenfermeria/en_proceso_teleseguimiento.html",
        {"teleseguimientos": teleseguimientos},
    )

def telezeguimientosrechazados(request):
    teleseguimientos = Teleseguimiento.objects.filter(estado="no_realizado")
    return render(
        request,
        "teleenfermeria/rechazados_teleseguimiento.html",
        {"teleseguimientos": teleseguimientos},
    )

def detalleteleseguimiento(request, teleseguimiento_id):
    teleseguimiento = get_object_or_404(Teleseguimiento, id=teleseguimiento_id)
    seguimientos = Seguimiento.objects.filter(teleseguimiento=teleseguimiento)
    
    
    return render(
        request,
        "teleenfermeria/detalle_teleseguimiento.html",
        {"teleseguimiento": teleseguimiento, "seguimientos": seguimientos},       
    )

def modificar_consentimiento(request, teleseguimiento_id, nuevo_estado):
    teleseguimiento = get_object_or_404(Teleseguimiento, pk=teleseguimiento_id)
    teleseguimiento.consentimiento_seguimiento = nuevo_estado
    if nuevo_estado == "aceptado":
        teleseguimiento.estado = "en_proceso"
    elif nuevo_estado == "Rechazado":
        teleseguimiento.estado = "no_realizado"
    teleseguimiento.save()
    return redirect('teleenfermeria:detalleteleseguimiento', teleseguimiento_id=teleseguimiento_id)


def crearseguimiento(request, teleseguimiento_id):
    teleseguimiento = get_object_or_404(Teleseguimiento, id=teleseguimiento_id)
    if request.method == "POST":
        form = SeguimientoForm(request.POST)
        if form.is_valid():
            seguimiento = form.save(commit=False)
            seguimiento.teleseguimiento = teleseguimiento
            seguimiento.usuario = request.user
            seguimiento.save()
            # Redirigir a la vista de detalle del teleseguimiento
            return redirect(
                "teleenfermeria:detalleteleseguimiento",
                teleseguimiento_id=teleseguimiento_id,
            )
    else:
        form = SeguimientoForm()
    return render(
        request,
        "teleenfermeria/crear_seguimiento.html",
        {"form": form, "teleseguimiento": teleseguimiento},
    )
