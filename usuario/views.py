# usuario/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.db.models import Q
from .models import Usuario
from reserva.models import Reserva, ReservaAsiento

def clientesForm(request):
    return render(request, 'crear_cliente.html')

def registro_cliente_desde_login(request):
    if request.method == 'POST':
        return crear_cliente(request, desde_login=True)  # Pasar el parámetro
    return render(request, 'lista_clientes.html')

def crear_cliente(request, desde_login=False):
    if request.method == 'POST':
        nombre = request.POST.get('nombre').title()
        apellido = request.POST.get('apellido').title()
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion').title()
        contraseña = request.POST.get('contraseña')  # Asegúrate de que este nombre coincida con tu formulario
        repetir_contraseña = request.POST.get('repetir_contraseña')  # Asegúrate de que este nombre coincida

        # Verificar si las contraseñas coinciden
        if contraseña != repetir_contraseña:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'crear_cliente.html', {
                'nombre': nombre,
                'apellido': apellido,
                'email': email,
                'telefono': telefono,
                'direccion': direccion,
            })

        try:
            # Crear el nuevo cliente
            usuario = Usuario.objects.create_user(
                email=email,
                password=contraseña,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                direccion=direccion,
                tipo_usuario='cliente'  # Asegúrate de que el tipo de usuario sea 'cliente'
            )
            messages.success(request, "Cliente creado con éxito.")
        except Exception as e:
            messages.error(request, f"Error al crear el cliente: {str(e)}")

    # Redireccionamiento después de crear el usuario
        if desde_login:
            return redirect('login')  # Redirige al login si el registro es desde la página de login
        elif request.user.is_staff:
            return redirect('lista_cliente')  # Redirige a la lista de clientes si es staff
        else:
            return redirect('index')  # Redirige a otra página si no es staff

def actualizar_cliente(request, id):
    cliente = Usuario.objects.get(id=id)
    data = {
        'cliente': cliente
    }
    
    if request.method == 'POST':
        # Obtén los datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')

        # Actualiza los campos del cliente
        cliente.nombre = nombre
        cliente.apellido = apellido
        cliente.email = email
        cliente.telefono = telefono
        cliente.direccion = direccion
        cliente.save()

        messages.success(request, "Cliente actualizado con éxito.")
        return redirect('lista_cliente')  # Redirige a la lista de clientes
    
    return render(request, 'actualizar_cliente.html', data)

def consultar_clientes(request):
    clientes = Usuario.objects.filter(tipo_usuario = "cliente")
    
    data = {
        "cliente" : clientes
    }
    
    return render(request, 'lista_clientes.html', data)

def custom_login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contraseña = request.POST.get('contraseña') 
        
        # Validar campos vacíos
        if not correo or not contraseña:
            messages.error(request, 'Por favor complete ambos campos.')
            return render(request, 'login.html')
        
        user = authenticate(request, email=correo, password=contraseña)
        
        if user is not None:
            login(request, user)
            print(f"Usuario autenticado: {user} con tipo_usuario: {user.tipo_usuario}")
            
            next_url = request.GET.get('next')
            
            if next_url:
                return redirect(next_url)
            else:
                if user.is_staff or user.tipo_usuario == 'personal':
                    return redirect('index')
                else:
                    return redirect('index')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')
    
    return render(request, 'login.html')

def mis_reservas(request):
    usuario = request.user
    search_query = request.GET.get("searchReserva", "")
    
    reservas = Reserva.objects.filter(
        cliente__id=usuario.id
    ).annotate(
        asientos_reservados=Count('reservas_asientos')  # Contamos el número de asientos reservados
    ).select_related('funcion', 'funcion__obra').filter(
        Q(funcion__fecha__icontains=search_query) |
        Q(funcion__hora__icontains=search_query) |
        Q(fecha_reserva__icontains=search_query)    
    ).values(
        'funcion__id',
        'funcion__fecha',
        'funcion__hora',
        'fecha_reserva',
        'id',
        'funcion__obra__nombre',
        'asientos_reservados'
    ).order_by('id')
    
    data = {
        'reservas': reservas
    }
    
    return render(request, "mis_reservas.html", data)