from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Reserva
from asiento.models import Asiento
from funciones.models import Funcion
from usuario.models import Usuario
from reserva.models import Reserva, ReservaAsiento
from datetime import datetime

def modificarFecha(fecha_reserva):
    fecha_reserva = datetime.strptime(fecha_reserva, "%d/%m/%Y")
    fecha_formateada = fecha_reserva.date()
    return fecha_formateada

#Creacion de cliente
def nuevaReserva(request):
    usuario = request.user
    id_asientos_reservados = request.POST.getlist('asientos_reservados')
    fecha_reserva = datetime.now().date()
    funcion_id = request.POST.get('id_funcion')
    usuario_especifico = Usuario.objects.get(id = usuario.id)
    funcion_especifica = Funcion.objects.get(id=int(funcion_id))
    
    reserva = Reserva.objects.create(
            fecha_reserva=fecha_reserva, 
            funcion=funcion_especifica,
            cliente=usuario_especifico
        )
    
    # Guardar los IDs de los asientos como objetos de la clase ReservaAsiento
    for asiento_id in id_asientos_reservados:
        asiento = Asiento.objects.get(id=int(asiento_id))
        ReservaAsiento.objects.create(
            reserva=reserva,
            asiento=asiento,
            estado=False  # Estado en ReservaAsiento, asumiendo que 'False' significa que el asiento está reservado
        )
    
    return redirect('mis_reservas')

def precio_total(total_asientos, obra_precio):
    precio_total = total_asientos * float(obra_precio)
    precio_total_formateado = "{:.2f}".format(precio_total)
    return precio_total_formateado

def confirmarFormReserva(request, funcion_id):
    if request.method == 'POST':
        usuario = request.user
        fechaReserva = datetime.now().date()
        id_funcion = funcion_id
        datos_funcion = Funcion.objects.get(id = id_funcion)
        funcion_fecha = datos_funcion.fecha
        funcion_hora = datos_funcion.hora
        obra_nombre = datos_funcion.obra.nombre
        obra_precio = datos_funcion.obra.precio
        id_asientos_seleccionados = request.POST.getlist('asientos_seleccionados') # ['1', '2', '3']
        print(id_asientos_seleccionados)
        # Validar que la funcion existe
        try:
            funcion = Funcion.objects.get(id=funcion_id)
        except Funcion.DoesNotExist:
            # Manejo del error si la funcion no existe
            return render(request, 'reserva_confirmacion.html', {'error': 'Funcion no encontrada'})
        
        # Filtra los asientos utilizando los IDs obtenidos
        asientos_ocupados  = ReservaAsiento.objects.filter(
            reserva__funcion=funcion,
            asiento__id__in=id_asientos_seleccionados, 
            estado=False
        )
        ids_ocupados = [str(asiento.asiento.id) for asiento in asientos_ocupados]
        asientos_no_ocupados = [
            id_asiento for id_asiento in id_asientos_seleccionados if id_asiento not in ids_ocupados
        ]
        asientos = Asiento.objects.filter(id__in = asientos_no_ocupados)
        
        total_asientos = len(asientos_no_ocupados)
        total_reserva = precio_total(total_asientos, obra_precio)  # Calcula el total de la reserva
        
        # Prepara los datos para renderizar
        data = {
            'usuario' : usuario,
            'fechaReserva': fechaReserva,
            'id_funcion': id_funcion,
            'funcion_fecha': funcion_fecha,
            'funcion_hora': funcion_hora,
            'obra_nombre': obra_nombre,
            "obra_precio": obra_precio,
            'asientos_seleccionados': asientos,
            'total_asientos': total_asientos,
            'total_reserva': total_reserva,
        }
        
        return render(request, 'reserva_confirmacion.html', data)
    
    return render(request, 'reserva_confirmacion.html')

def confEditarReserva(request, reserva_id):
    if request.method == 'POST':
        usuario = request.user
        funcion_id = request.POST.get('funcion_id')
        print(f"Funcion ID: {funcion_id}")
        datos_funcion = Funcion.objects.get(id = funcion_id)
        obra_nombre = datos_funcion.obra.nombre
        obra_precio = datos_funcion.obra.precio
        id_asientos_seleccionados = request.POST.getlist('asientos_seleccionados') # ['1', '2', '3']
        reserva = get_object_or_404(Reserva, id=reserva_id)
        id_reserva = reserva.id
        asientos_reservados = reserva.reservas_asientos.all()
    
        # Crear una lista con los ID y numero_asiento
        # Crear una lista con los ID y numero_asiento de los asientos reservados
        lista_asientos_reservados = [
            (reserva_asiento.id, reserva_asiento.asiento.id, reserva_asiento.asiento.numero_asiento)
            for reserva_asiento in asientos_reservados
        ]

        # Validar que la ruta existe
        funcion = get_object_or_404(Funcion, id=funcion_id)

        # Filtrar los asientos ocupados por la ruta
        asientos_ocupados = ReservaAsiento.objects.filter(
            reserva__funcion=funcion,
            estado=False  # Esto asume que 'estado' False significa que el asiento está ocupado
        ).exclude(reserva__id=reserva_id)

        # Crear un conjunto de IDs ocupados y reservados
        ids_ocupados = [str(asiento.asiento.id) for asiento in asientos_ocupados]
        asientos_seleccionados = [
            id_asiento for id_asiento in id_asientos_seleccionados if id_asiento not in ids_ocupados
        ]

        asientos = Asiento.objects.filter(id__in = asientos_seleccionados)
    
        total_asientos = len(asientos_seleccionados)  # Esto debería ser 2 para asientos 5 y 6
        total_reserva_antigua = precio_total(len(lista_asientos_reservados), obra_precio)
        total_reserva = precio_total(total_asientos, obra_precio)  # Calcula el total de la reserva
        
        # Prepara los datos para renderizar
        data = {
            'id_reserva': id_reserva,
            'usuario' : usuario,
            'funcion': datos_funcion,
            'obra_nombre': obra_nombre,
            'obra_precio': obra_precio,
            'lista_asientos_reservados': lista_asientos_reservados,
            'asientos_seleccionados': asientos,
            'total_asientos': total_asientos,
            'total_reserva': total_reserva,
        }
        
        return render(request, 'reserva_formEdit.html', data)
    
    return render(request, 'reserva_formEdit.html')

def editarReserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    asientos_reservados = reserva.reservas_asientos.all()
    
    lista_asientos_reservados = []
    for reserva_asiento in asientos_reservados:
        id_reserva_asiento = reserva_asiento.id
        id_asiento = reserva_asiento.asiento.id
        numero_asiento = reserva_asiento.asiento.numero_asiento
        lista_asientos_reservados.append((id_reserva_asiento, id_asiento, numero_asiento))
    
    id_asientos_reservados = request.POST.getlist('asientos_reservados')
    
    eliminar_registros = ReservaAsiento.objects.filter(reserva_id=reserva_id).delete()
    
    # Guardar los IDs de los asientos como objetos de la clase ReservaAsiento
    for asiento_id in id_asientos_reservados:
        asiento = Asiento.objects.get(id=int(asiento_id))
        ReservaAsiento.objects.create(
            reserva=reserva,
            asiento=asiento,
            estado=False  # Estado en ReservaAsiento, asumiendo que 'False' significa que el asiento está reservado
        )
    
    return redirect('mis_reservas')

def cancelar_reserva (request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    eliminar_registros = ReservaAsiento.objects.filter(reserva_id=reserva_id)
    eliminar_registros.delete()
    
    return redirect('mis_reservas')