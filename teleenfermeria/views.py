from django.shortcuts import render, redirect, get_object_or_404
from pacientes.models import Paciente
from .models import (
    Teleseguimiento,
    Seguimiento,
    Prescripcion,
    SolicitudTurno,
    Turno,
)
from django.db.models import Count
from .forms import (
    DiagnosticoForm,
    TeleseguimientoForm,
    FiltrarTeleseguimientoForm,
    SeguimientoForm,
    PrescripcionForm,
    AsignarTurnoForm,
)

from django.utils.timezone import now
from users.models import User
from datetime import timedelta, datetime
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from datetime import date
from django.db.models import Q


def group_required(*group_names):
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url="/no_permisos/")


def is_administrativo(user):
    return user.groups.filter(name="administrativo").exists() | user.is_superuser


def user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


def no_permisos(request):
    return render(request, "teleenfermeria/no_permisos.html")


@login_required
@group_required("Administrativo")
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


@login_required
@group_required("Teleenfermeria", "Administrativo")
def derivadosteleseguimiento(request):
    teleseguimientos = Teleseguimiento.objects.filter(estado="Derivado")

    # Filtrar teleseguimientos que no tienen seguimientos
    teleseguimientos_sin_seguimiento = teleseguimientos.exclude(
        id__in=Seguimiento.objects.values("teleseguimiento")
    )

    for teleseguimiento in teleseguimientos_sin_seguimiento:
        teleseguimiento.tiempo_espera = now() - teleseguimiento.fecha_solicitud

    return render(
        request,
        "teleenfermeria/derivados_teleseguimiento.html",
        {"teleseguimientos": teleseguimientos_sin_seguimiento},
    )


@login_required
@group_required("Teleenfermeria", "Administrativo")
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


@login_required
@group_required("Teleenfermeria", "Administrativo")
def telezeguimientosrechazados(request):
    teleseguimientos = Teleseguimiento.objects.filter(estado="no_realizado")
    return render(
        request,
        "teleenfermeria/rechazados_teleseguimiento.html",
        {"teleseguimientos": teleseguimientos},
    )


def televacunas(request, teleseguimiento_id):
    teleseguimiento = get_object_or_404(Teleseguimiento, id=teleseguimiento_id)
    if request.method == "POST":
        teleseguimiento.vacunas = request.POST.get("vacunas")
        teleseguimiento.save()
        return redirect(
            "teleenfermeria:detalleteleseguimiento",
            teleseguimiento_id=teleseguimiento_id,
        )


def detalleteleseguimiento(request, teleseguimiento_id):
    teleseguimiento = get_object_or_404(Teleseguimiento, id=teleseguimiento_id)
    seguimientos = Seguimiento.objects.filter(teleseguimiento=teleseguimiento)
    prescripciones = Prescripcion.objects.filter(teleseguimiento=teleseguimiento)
    turnos_aceptados = Turno.objects.filter(
        solicitud_turno__teleseguimiento=teleseguimiento
    )
    hoy = date.today()

    # Cálculo de la edad en años y meses
    fecha_nacimiento = teleseguimiento.paciente.fecha_nacimiento
    edad_years = hoy.year - fecha_nacimiento.year
    edad_months = hoy.month - fecha_nacimiento.month

    # Ajuste si el mes actual es anterior al mes de nacimiento
    if edad_months < 0:
        edad_years -= 1
        edad_months += 12

    # Ajuste si aún no ha cumplido el día de nacimiento este año
    if hoy.day < fecha_nacimiento.day:
        edad_months -= 1
        if edad_months < 0:
            edad_years -= 1
            edad_months += 12

    turnos_aceptados = Turno.objects.filter(
        solicitud_turno__teleseguimiento=teleseguimiento
    )

    if request.method == "POST":
        form = DiagnosticoForm(request.POST, instance=teleseguimiento)
        if form.is_valid():
            form.save()
            return redirect(
                "teleenfermeria:detalleteleseguimiento",
                teleseguimiento_id=teleseguimiento_id,
            )
    else:
        form = DiagnosticoForm(instance=teleseguimiento)

    return render(
        request,
        "teleenfermeria/detalle_teleseguimiento.html",
        {
            "teleseguimiento": teleseguimiento,
            "seguimientos": seguimientos,
            "prescripciones": prescripciones,
            "turnos_aceptados": turnos_aceptados,
            "form": form,
            "edad_years": edad_years,
            "edad_months": edad_months,
        },
    )


@login_required
def modificar_consentimiento(request, teleseguimiento_id, nuevo_estado):
    teleseguimiento = get_object_or_404(Teleseguimiento, pk=teleseguimiento_id)

    # Normalizar el nuevo estado a minúsculas para comparar de manera consistente
    nuevo_estado = nuevo_estado.strip().lower()

    # Mapeo para manejar valores actuales y normalizados
    estado_map = {
        "aceptado": "aceptado",
        "rechazado": "Rechazado",  # Mantener la capitalización existente
        "en_espera": "En espera",
        "pasivo": "pasivo",
    }

    # Comprobar si el estado ingresado es válido (ignorando mayúsculas/minúsculas y espacios)
    if nuevo_estado in estado_map:
        teleseguimiento.consentimiento_seguimiento = estado_map[nuevo_estado]

        if nuevo_estado == "aceptado":
            teleseguimiento.estado = "en_proceso"
        elif nuevo_estado == "rechazado":
            teleseguimiento.estado = "no_realizado"
        else:
            teleseguimiento.estado = "derivado"  # Si es "en espera" o "pasivo"

        teleseguimiento.save()
        return redirect(
            "teleenfermeria:detalleteleseguimiento",
            teleseguimiento_id=teleseguimiento_id,
        )
    else:
        # Si el nuevo estado no es válido, podrías agregar un mensaje de error
        return redirect(
            "teleenfermeria:detalleteleseguimiento",
            teleseguimiento_id=teleseguimiento_id,
        )


@login_required
@group_required("Teleenfermeria")
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
                "teleenfermeria:detalleteleseguimiento",
                teleseguimiento_id=teleseguimiento_id,
            )
    else:
        form = PrescripcionForm()
    return render(
        request,
        "teleenfermeria/agregar_prescripcion.html",
        {"form": form, "teleseguimiento": teleseguimiento},
    )


@login_required
@group_required("Teleenfermeria", "Administrativo")
def teleseguimientosusuario(request):
    seguimientos = Seguimiento.objects.filter(usuario=request.user)
    teleseguimientos = Teleseguimiento.objects.filter(
        id__in=seguimientos.values("teleseguimiento_id")
    )
    return render(
        request,
        "teleenfermeria/teleseguimientos_usuario.html",
        {"teleseguimientos": teleseguimientos},
    )


@login_required
@group_required(
    "Teleenfermeria", "Administrativo"
)  # Asegúrate de que el usuario esté en el grupo adecuado
def teleseguimientos_mis_derivados(request):
    # Filtramos los teleseguimientos donde el agente logueado es el agente asignado
    teleseguimientos = Teleseguimiento.objects.filter(agente=request.user)

    return render(
        request,
        "teleenfermeria/teleseguimientos_misderivados.html",  # El nombre de tu template
        {"teleseguimientos": teleseguimientos},
    )


def solicitarturno(request, teleseguimiento_id):
    teleseguimiento = get_object_or_404(Teleseguimiento, id=teleseguimiento_id)

    # Calcular el inicio de la semana actual (lunes)
    now = localtime(timezone.now())
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    print(now)
    # Contar todas las solicitudes desde el inicio de la semana actual
    solicitudes_recientes = SolicitudTurno.objects.filter(
        fecha_solicitud__gte=start_of_week
    ).count()

    if solicitudes_recientes >= 10:
        return render(
            request,
            "teleenfermeria/solicitar_turno.html",
            {
                "teleseguimiento": teleseguimiento,
                "error": "No se pueden realizar más de 10 solicitudes de turno por semana.",
            },
        )

    if request.method == "POST":
        especialidad = request.POST.get("especialidad")
        imagen_orden = request.FILES.get("imagen_orden")
        # Crear la solicitud de turno
        solicitud_turno = SolicitudTurno.objects.create(
            teleseguimiento=teleseguimiento,
            especialidad=especialidad,
            imagen_orden=imagen_orden,
        )
        return redirect(
            "teleenfermeria:detalleteleseguimiento",
            teleseguimiento_id=teleseguimiento_id,
        )
    return render(
        request,
        "teleenfermeria/solicitar_turno.html",
        {"teleseguimiento": teleseguimiento},
    )


@login_required
@group_required("Turnera", "Teleenfermeria")
def turnosporsemana(request):
    """
    Vista que muestra las solicitudes de turno de una semana específica.
    """
    # Obtener la semana seleccionada del formulario
    week_str = request.GET.get("week")
    if week_str:
        selected_date = datetime.strptime(week_str + "-1", "%Y-W%W-%w")
    else:
        selected_date = localtime(now())

    # Calcular inicio/fin de semana
    start_of_week = selected_date - timedelta(days=selected_date.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

    # Obtener solicitudes de la semana seleccionada
    solicitudes_recientes = SolicitudTurno.objects.filter(
        fecha_solicitud__range=(start_of_week, end_of_week)
    ).order_by("-fecha_solicitud")

    context = {
        "solicitudes_recientes": solicitudes_recientes,
        "start_of_week": start_of_week,
        "end_of_week": end_of_week,
        "selected_week": selected_date.strftime("%Y-W%W"),
        "is_turnero": user_in_group(request.user, "Turnera"),
    }

    return render(request, "teleenfermeria/solicitudesrecientes.html", context)


@login_required
@group_required("Turnera")
def asignarturno(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudTurno, id=solicitud_id)
    if request.method == "POST":
        form = AsignarTurnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.solicitud_turno = solicitud
            turno.save()
            solicitud.estado = "confirmado"
            solicitud.save()
            return redirect("teleenfermeria:turnossemanales")
    else:
        form = AsignarTurnoForm()
    return render(
        request,
        "teleenfermeria/asignar_turno.html",
        {"form": form, "solicitud": solicitud},
    )


@login_required
@group_required("CordinadoraTeleseguimientos")
def administrar_teleseguimientos(request):
    grupo_teleenfermeria = Group.objects.get(name="Teleenfermeria")
    usuarios_teleenfermeria = User.objects.filter(groups=grupo_teleenfermeria)

    query = request.GET.get("q")
    usuario_seleccionado = request.GET.get("usuario")
    teleseguimientos = Teleseguimiento.objects.all()

    if query:
        teleseguimientos = teleseguimientos.filter(
            Q(paciente__nombre_completo__icontains=query)
            | Q(paciente__dni__icontains=query)
        )

    if usuario_seleccionado:
        seguimientos = Seguimiento.objects.filter(usuario=usuario_seleccionado)
        teleseguimientos = teleseguimientos.filter(
            id__in=seguimientos.values("teleseguimiento_id")
        )

    form = FiltrarTeleseguimientoForm(
        usuarios=usuarios_teleenfermeria, initial={"usuario": usuario_seleccionado}
    )

    context = {
        "form": form,
        "teleseguimientos": teleseguimientos,
        "query": query,
        "usuario_seleccionado": usuario_seleccionado,
    }
    return render(request, "teleenfermeria/administrar_teleseguimientos.html", context)


def rechazarsolicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudTurno, id=solicitud_id)
    solicitud.estado = "rechazado"
    solicitud.save()
    return redirect("teleenfermeria:turnossemanales")
