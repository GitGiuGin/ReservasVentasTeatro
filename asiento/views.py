from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from obra.models import Obra
from asiento.models import Asiento
from reserva.models import Reserva, ReservaAsiento
from funciones.models import Funcion
from datetime import datetime

# Create your views here.
def obtenerFechaActual(request):
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    return fecha_actual

def obtenerEstado(asiento_id, funcion_id):
    try:
        # Busca el estado en la tabla intermedia ReservaAsiento
        reserva_asiento = ReservaAsiento.objects.get(asiento_id=asiento_id, reserva__funcion_id=funcion_id)
        return "checked" if not reserva_asiento.estado else ""
    except ReservaAsiento.DoesNotExist:
        # Si no existe una reserva, significa que está disponible
        return ""

def verificarDisponibilidad(funcion_id):
    asientos_disponibles = Asiento.objects.exclude(
        reservas_asientos__reserva__funcion_id=funcion_id, 
        reservas_asientos__estado=False
    )
    
    return asientos_disponibles

@login_required(login_url='login')
def formSelectAsiento(request, funcion_id):
    usuario = request.user
    fecha_actual = obtenerFechaActual(request)
    funcion = Funcion.objects.get(id = funcion_id)
    obra = funcion.obra
    asientos_disponibles = verificarDisponibilidad(funcion_id = funcion.id)
    total_asientos_disponibles = asientos_disponibles.count()
    asientos = Asiento.objects.all()
    for asiento in asientos:
        asiento.estado_check = obtenerEstado(asiento.id, funcion.id)
    
    data = {
        "funcion": funcion,
        "obra": obra,
        "fecha_actual": fecha_actual,
        "asientos": asientos,
        "usuario": usuario,
        "asientos_disponibles" : total_asientos_disponibles
    }
    
    return render(request, 'seleccion_asiento.html', data)

def formEditAsiento(request, reserva_id, funcion_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    asientos_reservados = reserva.reservas_asientos.all()
    usuario = request.user
    funcion = Funcion.objects.get(id=funcion_id)
    obra = reserva.funcion.obra
    asientos = Asiento.objects.all()
    for asiento in asientos:
        asiento.estado_check = obtenerEstado(asiento.id, funcion.id)
        
    # Contador de asientos disponibles
    asientos_disponibles = verificarDisponibilidad(funcion_id = funcion.id)
    total_asientos_disponibles = asientos_disponibles.count()
    # print(f"Reserva ID: {reserva.id}")
    # Crear una lista con los ID y numero_asiento
    lista_asientos_reservados = []
    for reserva_asiento in asientos_reservados:
        id_reserva_asiento = reserva_asiento.id
        id_asiento = reserva_asiento.asiento.id
        numero_asiento = reserva_asiento.asiento.numero_asiento
        lista_asientos_reservados.append((id_reserva_asiento, id_asiento, numero_asiento))

    # Marcar asientos reservados solo en el contexto, sin cambios permanentes
    for asiento in asientos:
        if asiento.id in [id_asiento for _, id_asiento, _ in lista_asientos_reservados]:
            asiento.estado_check = ""
    
    # CREAR UN METODO PARA ELIMINAR REGISTROS DE LA TABLA M:N
    id_asientos_reservados = request.POST.getlist('asientos_reservados')
    for asiento_id in id_asientos_reservados:
        asiento_edit = Asiento.objects.get(id=int(asiento_id))
        ReservaAsiento.objects.create(
            reserva=reserva,
            asiento=asiento_edit,
            estado=False
        )
    
    data = {
        'reserva_id': reserva.id,
        'usuario': usuario,
        'funcion': funcion,
        'obra': obra,
        'asientos': asientos,
        'fecha_actual': reserva.fecha_reserva,
        'asientos_disponibles' : total_asientos_disponibles,
        'asientos_reservados' : lista_asientos_reservados
    }
    
    return render(request, "editar_asientos.html", data)