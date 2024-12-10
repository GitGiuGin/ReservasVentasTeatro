from django.shortcuts import render
from datetime import datetime
from obra.models import Obra
from funciones.models import Funcion

from datetime import datetime

def index(request):
    # Obtener la fecha actual
    today = datetime.now()

    # Filtrar las obras con estado True
    obras = Obra.objects.filter(estado=True)

    # Filtrar las funciones por obra que tengan una fecha mayor o igual a hoy
    funciones_por_obra = {
        obra: Funcion.objects.filter(obra=obra, fecha__gte=today)
        for obra in obras
        if Funcion.objects.filter(obra=obra, fecha__gte=today).exists()
    }
    
    data = {
        "obras": obras,
        "funciones_por_obra": funciones_por_obra
    }

    return render(request, "base.html", data)


