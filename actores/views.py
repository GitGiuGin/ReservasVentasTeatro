from django.shortcuts import render, redirect
from django.contrib import messages
from actores.models import Actores

def crear_actor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre').title()
        apellido = request.POST.get('apellido').title()
        edad = request.POST.get('edad')
        
    try:
        actor = Actores.objects.create(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
        )
        messages.success(request, "Actor creado con éxito.")
        return redirect('lista_actor')  # Redirige a la lista de clientes
    except Exception as e:
        messages.error(request, f"Error al crear el actor: {str(e)}")
    
    return render(request, "crear_actor.html")

def actualizar_actor(request, id):
    actor = Actores.objects.get(id=id)
    data = {
        'actor': actor
    }
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        edad = request.POST.get('edad')

        # Verificar si la edad es None o no es un número válido
        if edad is None or edad.strip() == '':
            messages.error(request, "La edad es requerida y debe ser un número válido.")
            return render(request, "actualizar_actor.html", data)

        # Convertir edad a entero
        try:
            actor.edad = int(edad)
        except ValueError:
            messages.error(request, "Por favor, ingresa una edad válida.")
            return render(request, "actualizar_actor.html", data)

        actor.nombre = nombre
        actor.apellido = apellido
        actor.save()

        messages.success(request, "Actor actualizado con éxito.")
        return redirect('lista_actor')
    
    return render(request, "actualizar_actor.html", data)

def consultar_actor(request):
    actor = Actores.objects.all()
    
    data = {
        "actor" : actor
    }
    
    return render(request, "lista_actor.html", data)