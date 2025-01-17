from django.shortcuts import render, redirect
from pacientes.models import Paciente
from .models import Teleseguimiento

def solicitarteleseguimiento(request, id):
    paciente = Paciente.objects.get(id=id)
    if request.method == 'POST':
        teleseguimiento = Teleseguimiento(paciente=paciente, descripcion=request.POST['descripcion'])
        teleseguimiento.save()
        return redirect('teleenfermeria:teleseguimiento', id=teleseguimiento.id)
    return render(request, 'teleenfermeria/solicitarteleseguimiento.html', {'paciente': paciente})
