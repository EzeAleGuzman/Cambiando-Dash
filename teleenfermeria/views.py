from django.shortcuts import render, redirect, get_object_or_404
from pacientes.models import Paciente
from .models import Teleseguimiento
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


def detalleteleseguimiento(request, teleseguimiento_id):
    teleseguimiento = get_object_or_404(Teleseguimiento, id=teleseguimiento_id)
    return render(
        request,
        "teleenfermeria/detalle_teleseguimiento.html",
        {"teleseguimiento": teleseguimiento},
    )


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
