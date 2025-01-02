# En views.py
from django.views.generic import ListView
from .models import Cama, Servicio, Ubicacion
from django.shortcuts import render


class DashboardView(ListView):
    model = Cama
    template_name = "gestioncamas/dashboard.html"

    def get_queryset(self):
        return Cama.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_camas = Cama.objects.count()
        ocupacion = Cama.objects.filter(estado="OCUPADA").count()

        # Asegurarse de que total_camas no sea cero
        context["total_camas"] = total_camas if total_camas > 0 else 1
        context["ocupacion"] = ocupacion if ocupacion is not None else 0

        # Calcular la capacidad disponible
        context["capacidad_disponible"] = context["total_camas"] - context["ocupacion"]
        context["alertas_criticas"] = 0  # Cambia según tu lógica

        return context


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
    ubicacion = Ubicacion.objects.get(id=ubicacion_id)

    # Obtener las camas asociadas a esa ubicación
    camas = Cama.objects.filter(ubicacion=ubicacion).select_related("paciente")

    # Filtrar pacientes asignados
    camas_con_paciente = camas.filter(paciente__isnull=False)
    camas_libres = camas.filter(paciente__isnull=True)

    context = {
        "ubicacion": ubicacion,
        "camas_con_paciente": camas_con_paciente,
        "camas_libres": camas_libres,
    }

    return render(request, "gestioncamas/ubicacion_detalle.html", context)
