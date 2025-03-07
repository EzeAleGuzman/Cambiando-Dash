from django.shortcuts import render,get_object_or_404, redirect
from .models import *
from .forms import *
from gestioncamas.models import PacienteCama
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def crearaislamiento(request, paciente_id):
    paciente_cama = get_object_or_404(PacienteCama, paciente_id=paciente_id)
    tipos_aislamientos =TipoAislamiento.objects.all()
    if request.method == "POST":
        form = AislamientoForm(request.POST)
        if form.is_valid():
            aislamiento = form.save(commit=False)
            aislamiento.fecha_inicio = timezone.now()
            aislamiento.cama_paciente = paciente_cama
            aislamiento.save()
            return redirect('pacientes:detallepaciente', id=paciente_id)
        else:
            messages.error(request, 'Error al guardar el aislamiento')
    else:
        form = AislamientoForm()
    return render(request, 'aislamientos/crearaislamiento.html', {'form': form, 'paciente_id': paciente_id, 'tipos_aislamientos': tipos_aislamientos})

def finalizaraislamiento(request, aislamiento_id):
    aislamiento = get_object_or_404(Aislamiento, id=aislamiento_id)
    paciente_id = aislamiento.cama_paciente.paciente.id
    
    if not aislamiento.fecha_fin:
        aislamiento.fecha_fin = timezone.now()
        aislamiento.save()
        messages.success(request, 'Aislamiento finalizado exitosamente')
    else:
        messages.warning(request, 'Este aislamiento ya fue finalizado')
    
    return redirect('pacientes:detallepaciente', id=paciente_id)