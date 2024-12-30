# En views.py
from django.views.generic import ListView
from .models import Cama

class DashboardView(ListView):
    model = Cama
    template_name = 'gestioncamas/dashboard.html'

    def get_queryset(self):
        return Cama.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_camas = Cama.objects.count()
        ocupacion = Cama.objects.filter(estado='OCUPADA').count()

        # Asegurarse de que total_camas no sea cero
        context['total_camas'] = total_camas if total_camas > 0 else 1
        context['ocupacion'] = ocupacion if ocupacion is not None else 0

        # Calcular la capacidad disponible
        context['capacidad_disponible'] = context['total_camas'] - context['ocupacion']
        context['alertas_criticas'] = 0  # Cambia según tu lógica

        return context
