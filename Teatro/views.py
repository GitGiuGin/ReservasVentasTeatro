from django.shortcuts import render
from obra.models import Obra
from funciones.models import Funcion

def index (request):
    obras = Obra.objects.filter(estado = True)
    funciones_por_obra = {obra: Funcion.objects.filter(obra=obra) for obra in obras}
    data = {
        "obras" : obras,
        "funciones_por_obra": funciones_por_obra
    }
    return render(request, "base.html", data)

