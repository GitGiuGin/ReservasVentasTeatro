from django.shortcuts import render, redirect
from django.contrib import messages
from categoria.models import Categoria

def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre').title()
        
        # Validar y crear la obra
        try:
            categoria = Categoria(
                nombre=nombre,
            )
            categoria.save()
            # Asignar los actores seleccionados a la obra
            messages.success(request, "Categoria creada con éxito.")
            return redirect('lista_categoria')  # Redirigir a la vista deseada
        except Exception as e:
            messages.error(request, f"Error al crear la obra: {str(e)}")
    
    return render(request, "crear_categoria.html")

def consultar_categoria(request):
    categorias = Categoria.objects.all()
    
    # Filtro de búsqueda
    search_query = request.GET.get('searchCategoria')
    if search_query:
        categorias = categorias.filter(nombre__icontains=search_query)
    
    data = {
        "categorias": categorias
    }
    
    return render(request, "lista_categoria.html", data)

def actualizar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    
    data = {
        "categoria" : categoria,
    }
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre').title()
    
        try:
            categoria.nombre = nombre
            categoria.save()
            
            return redirect('lista_categoria')
        except Exception as e:
            messages.error(request, f"Error al actualizar la obra: {str(e)}")
    
    return render(request, "actualizar_categoria.html", data)