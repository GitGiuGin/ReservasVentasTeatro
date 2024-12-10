from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from reserva.models import Reserva
from pago.models import Pago

# Create your views here.
def registrar_pago(request, reserva_id):
    if request.method == 'POST':
        reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user)
        total_a_pagar = request.POST.get('total_a_pagar')
        
        # Verifica si ya existe un pago asociado
        if hasattr(reserva, 'pago'):
            messages.error(request, 'El pago para esta reserva ya ha sido registrado.')
            return redirect('mis_reservas')

        # Obtiene los datos del formulario
        archivo_pago = request.FILES.get('pdf_documento')

        if archivo_pago:
            # Crear un nuevo registro de Pago
            pago = Pago.objects.create(
                reserva=reserva,
                monto_total=total_a_pagar,
                metodo_pago="Comprobante de Pago",
                archivo_pago=archivo_pago
            )
            reserva.estado = 'Pagado'  # Cambia el estado de la reserva
            reserva.save()
            messages.success(request, 'El pago ha sido registrado exitosamente.')
        else:
            messages.error(request, 'Por favor, complete todos los campos.')

    return redirect('mis_compras')