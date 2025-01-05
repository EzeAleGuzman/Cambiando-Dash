
from .models import Cama, Servicio, Ubicacion, PacienteCama
from django.shortcuts import render, get_object_or_404


def Dashbord(request):
    #obtener datos de los servicios
    servicios = Servicio.objects.all()
    total_servicios = servicios.count()
    capacidad_total = 0
    ocupacion_total = 0
   
    for servicio in servicios:
        ubicaciones = Ubicacion.objects.filter(servicio=servicio)
        capacidad_servicio = sum(ubicacion.capacidad for ubicacion in ubicaciones)
        camas_ocupadas_servicio = sum(Cama.objects.filter(ubicacion=ubicacion, estado="OCUPADA").count() for ubicacion in ubicaciones)

        capacidad_total += capacidad_servicio
        ocupacion_total += camas_ocupadas_servicio

        servicio.capacidad_total = capacidad_servicio
        servicio.ocupacion_total = camas_ocupadas_servicio
    
    nivel_ocupacion = round((ocupacion_total / capacidad_total) * 100, 2) if capacidad_total != 0 else 0


    #obtener datos de ubicaciones
    ubicaciones = Ubicacion.objects.all()
    total_ubicaciones = ubicaciones.count()
    habitaciones = ubicaciones.filter(tipo="HABITACION").count()
    area = ubicaciones.filter(tipo="AREA").count()

    #obtener datos de camas
    camas = Cama.objects.all()
    total_camas = camas.count()
    camas_ocupadas = camas.filter(estado="OCUPADA").count()
    camas_disponibles = total_camas - camas_ocupadas

    context = {
        "total_servicios": total_servicios,
        "capacidad_total": capacidad_total,
        "ocupacion_total": ocupacion_total,
        "nivel_ocupacion": nivel_ocupacion,
        "total_camas": total_camas,
        "camas_ocupadas": camas_ocupadas,
        "camas_disponibles": camas_disponibles,
        "servicios": servicios,
        "camas": camas,
        "ubicaciones": ubicaciones,
    }
    return render(request, "gestioncamas/dashboard.html", context)


def habitaciones_por_servicio(request):
    servicios = Servicio.objects.all()
    data = []

    for servicio in servicios:
        ubicaciones = servicio.ubicacion_set.all()  # Obtener todas las ubicaciones asociadas al servicio
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
    camas_con_paciente = PacienteCama.objects.filter(cama__in=camas, paciente__isnull=False)
    camas_libres = camas.filter(pacientecama__isnull=True)

    context = {
        "ubicacion": ubicacion,
        "camas_con_paciente": camas_con_paciente,
        "camas_libres": camas_libres,
    }

    return render(request, "gestioncamas/ubicacion_detalle.html", context)


