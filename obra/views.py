from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from obra.models import Obra
from actores.models import Actores
from funciones.models import Funcion
from asiento.views import verificarDisponibilidad

# Create your views here.
def crear_obra(request):
    actores = Actores.objects.all()  # Obtener la lista de actores
    data = {
        "actores": actores
    }

    if request.method == 'POST':
        nombre = request.POST.get('nombre').title()
        precio = request.POST.get('precio')
        imagen = request.FILES.get('imagen')
        actores_ids = request.POST.getlist('actores')

        print(f"Nombre: {nombre}, Precio: {precio}, Imagen: {imagen}, Actores IDs: {actores_ids}")
        
        # Validar y crear la obra
        if nombre and precio and imagen:
            try:
                precio = float(precio)
                obra = Obra(
                    nombre=nombre,
                    precio=precio,
                    imagen=imagen
                )
                obra.save()

                # Asignar los actores seleccionados a la obra
                obra.actores.set(actores_ids)
                obra.save()

                messages.success(request, "Obra creada con éxito.")
                return redirect('lista_obra')  # Redirigir a la vista deseada
            except Exception as e:
                messages.error(request, f"Error al crear la obra: {str(e)}")
        else:
            messages.error(request, "Todos los campos son obligatorios.")

    return render(request, "crear_obra.html", data)

@login_required(login_url='login')
def detalle_obra(request, id):
    obra = Obra.objects.get(id=id)
    funciones_por_obra = Funcion.objects.filter(obra=obra)
    actores = Actores.objects.all()
    actores_seleccionados = obra.actores.all()
    
    total_asientos_disponibles_por_funcion = {}

    for funcion in funciones_por_obra:
        asientos_disponibles = verificarDisponibilidad(funcion_id=funcion.id)
        total_asientos_disponibles = asientos_disponibles.count()
        print(f"Función ID: {funcion.id} - Asientos Disponibles: {total_asientos_disponibles}")
        total_asientos_disponibles_por_funcion[funcion.id] = total_asientos_disponibles

    data = {
        "obra": obra,
        "actores": actores,
        "actores_seleccionados": actores_seleccionados,
        "funciones": funciones_por_obra,
        "total_asientos_disponibles_por_funcion": total_asientos_disponibles_por_funcion
    }

    return render(request, "detalle_obra.html", data)

def actualizar_obra(request, id):
    obra = Obra.objects.get(id=id)
    actores = Actores.objects.all()
    actores_seleccionados = obra.actores.all()
    
    data = {
        "obra" : obra,
        "actores" : actores,
        "actores_seleccionados" : actores_seleccionados
    }
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre').title()
        precio = request.POST.get('precio')
        imagen = request.FILES.get('imagen')
        actores_ids = request.POST.getlist('actores')

        # Actualizar los datos de la obra
        try:
            obra.nombre = nombre
            obra.precio = float(precio)
            
            if imagen:  # Actualizar la imagen solo si se proporciona una nueva
                obra.imagen = imagen
            
            obra.save()

            # Asignar los actores seleccionados a la obra
            obra.actores.set(actores_ids)
            obra.save()

            messages.success(request, "Obra actualizada con éxito.")
            return redirect('lista_obra')  # Redirigir a la vista deseada
        except Exception as e:
            messages.error(request, f"Error al actualizar la obra: {str(e)}")

    
    return render(request, "actualizar_obra.html", data)

def consultar_obras(request):
    obras = Obra.objects.prefetch_related('funciones').all()  # Pre-fetch de funciones relacionadas
    
    # Filtro de búsqueda
    search_query = request.GET.get('searchObra')
    if search_query:
        obras = obras.filter(nombre__icontains=search_query)
    
    data = {
        "obra": obras
    }
    
    return render(request, "lista_obra.html", data)

def cambiar_estado(request, obra_id):
    # Obtener la obra usando el ID
    obra = get_object_or_404(Obra, id=obra_id)
    
    # Cambiar el estado de True a False o viceversa
    obra.estado = not obra.estado
    obra.save()
    
    # Redirigir a la lista de obras
    return redirect("lista_obra")