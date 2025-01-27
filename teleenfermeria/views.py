from django.shortcuts import render, redirect, get_object_or_404
from pacientes.models import Paciente
from .models import Teleseguimiento, Seguimiento, Prescripcion, Medicacion
from .forms import TeleseguimientoForm, SeguimientoForm, PrescripcionForm
from django.utils.timezone import now
from users.models import User

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
    for teleseguimiento in teleseguimientos:
        teleseguimiento.tiempo_espera = now() - teleseguimiento.fecha_solicitud

    return render(
        request,
        "teleenfermeria/derivados_teleseguimiento.html",
        {"teleseguimientos": teleseguimientos},
    )


def enprocesoteleseguimiento(request):
    teleseguimientos = Teleseguimiento.objects.filter(estado="en_proceso")
    for teleseguimiento in teleseguimientos:
        ultimo_seguimiento_fecha = teleseguimiento.fecha_ultimo_seguimiento()
        if ultimo_seguimiento_fecha:
            teleseguimiento.tiempo_espera = now() - ultimo_seguimiento_fecha
        else:
            teleseguimiento.tiempo_espera = None
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
    prescripciones = Prescripcion.objects.filter(teleseguimiento=teleseguimiento)
    

    return render(
        request,
        "teleenfermeria/detalle_teleseguimiento.html",
        {"teleseguimiento": teleseguimiento, "seguimientos": seguimientos, "prescripciones": prescripciones},
    )


def modificar_consentimiento(request, teleseguimiento_id, nuevo_estado):
    teleseguimiento = get_object_or_404(Teleseguimiento, pk=teleseguimiento_id)
    teleseguimiento.consentimiento_seguimiento = nuevo_estado
    if nuevo_estado == "aceptado":
        teleseguimiento.estado = "en_proceso"
    elif nuevo_estado == "Rechazado":
        teleseguimiento.estado = "no_realizado"
    teleseguimiento.save()
    return redirect(
        "teleenfermeria:detalleteleseguimiento", teleseguimiento_id=teleseguimiento_id
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



def agregar_prescripcion(request, teleseguimiento_id):
    teleseguimiento = get_object_or_404(Teleseguimiento, id=teleseguimiento_id)
    if request.method == "POST":
        form = PrescripcionForm(request.POST)
        if form.is_valid():
            prescripcion = form.save(commit=False)
            prescripcion.teleseguimiento = teleseguimiento
            prescripcion.save()
            return redirect(
                "teleenfermeria:detalleteleseguimiento", teleseguimiento_id=teleseguimiento_id
            )
    else:
        form = PrescripcionForm()
    return render(
        request,
        "teleenfermeria/agregar_prescripcion.html",
        {"form": form, "teleseguimiento": teleseguimiento},
    )

def teleseguimientosusuario(request):
    user = User.objects.filter(groups__name="Teleenfermeria").first()
    teleseguimientos = Teleseguimiento.objects.filter(usuario=request.user)
    return render(
        request,
        "teleenfermeria/teleseguimientos_usuario.html",
        {"teleseguimientos": teleseguimientos},
    )

def solicitarturno(request, teleseguimiento_id):
    teleseguimiento = get_object_or_404(Teleseguimiento, id=teleseguimiento_id)
    teleseguimiento.estado = "En Proceso"
    teleseguimiento.save()
    return redirect("teleenfermeria:detalleteleseguimiento", teleseguimiento_id=teleseguimiento_id)