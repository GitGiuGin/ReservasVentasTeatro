from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from obra.models import Obra
from funciones.models import Funcion

# Create your views here.
def crear_funcion (request):
    obras = Obra.objects.all()
    
    if request.method == "POST":
        obra_id = request.POST.get('selectObra')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        obra_seleccionada = Obra.objects.get(id = obra_id)
        nueva_funcion = Funcion(
            obra = obra_seleccionada,
            fecha = fecha,
            hora = hora
        )
        nueva_funcion.save()
        
        return redirect('index')
        
    data = {
        "obras": obras
    }
    return render(request, "crear_funcion.html", data)

def actualizar_funcion (request, obra_id, funcion_id):
    obra = Obra.objects.get(id = obra_id)
    funcion = Funcion.objects.get(id = funcion_id)
    
    
    
    data = {
        "obra": obra,
        "funcion": funcion
    }
    return render(request, "actualizar_funcion.html", data)

def editar_funcion(request):
    id_funcion = request.POST.get('id_funcion')
    id_obra = request.POST.get('id_obra')
    fecha = request.POST.get('fecha')
    hora = request.POST.get('hora')
    funcion = Funcion.objects.get(id = id_funcion)
    
    if funcion.fecha and funcion.hora:
        funcion.fecha = fecha
        funcion.hora = hora
    funcion.save()
    
    return redirect('detalle_obra', id=id_obra)

def eliminar_funcion(request, funcion_id):
    funcion = get_object_or_404(Funcion, id=funcion_id)
    id_obra = request.POST.get('id_obra')
    
    # Eliminar la función
    funcion.delete()
    messages.success(request, "Función eliminada exitosamente.")
    
    # Redirigir a la página de lista de funciones o a la página deseada
    return redirect('detalle_obra', id=funcion.obra.id)