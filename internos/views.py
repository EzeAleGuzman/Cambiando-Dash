from django.shortcuts import render
from .models import Interno
from .forms import InternoForm

def ver_interno(request):
    internos = Interno.objects.all().order_by('servicio')
    form = InternoForm()

    context = {
        'internos': internos,
        'form' : form,
        }
    return render(request, 'internos.html',context)

def home(request):
    return render(request, 'base.html')