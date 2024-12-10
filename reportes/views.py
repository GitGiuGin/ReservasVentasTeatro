from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count, Sum
from datetime import datetime
from weasyprint import HTML
from usuario.models import Usuario
from pago.models import Pago
import pytz

# Create your views here.
def vista_preliminar_reporte_clientes(request):
    # Filtrar solo los usuarios que son clientes
    clientes = Usuario.objects.filter(tipo_usuario='cliente')

    # Renderizar el HTML con los datos de los clientes
    return render(request, 'reporte_clientes.html', {'clientes': clientes})

def descargar_reporte_pdf(request):
    clientes = Usuario.objects.filter(tipo_usuario='cliente')
    administrador = request.user
    fecha_actual = datetime.now()

    data = {
        'clientes': clientes,
        'administrador': administrador,
        'now': fecha_actual
    }
    
    html_string = render_to_string('reporte_clientesPDF.html', data)
    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_clientes.pdf"'

    return response

def reporte_ventas(request):
    accion = request.GET.get('accion')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    nombre_obra = request.GET.get('nombre_obra')
    
    print(f"Fecha de inicio: {fecha_inicio}")
    print(f"Fecha de fin: {fecha_fin}")
    
    # Convertir las fechas a formato DateTime si son proporcionadas
    if fecha_inicio:
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    if fecha_fin:
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)

    # Filtrar los pagos según el rango de fechas
    if fecha_inicio and fecha_fin:
        resultados = Pago.objects.filter(fecha_pago__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        resultados = Pago.objects.filter(fecha_pago__gte=fecha_inicio)
    elif fecha_fin:
        resultados = Pago.objects.filter(fecha_pago__lte=fecha_fin)
    elif nombre_obra:
        resultados = Pago.objects.filter(reserva__funcion__obra__nombre__icontains=nombre_obra)
    else:
        resultados = Pago.objects.all()  # Si no hay filtros, se muestran todos los pagos
    
    reporte = Pago.objects.select_related(
        'reserva__cliente',
        'reserva__funcion__obra',
        'reserva__funcion',
    ).annotate(
        num_asientos_reservados=Count('reserva__reservas_asientos')
    ).order_by('-fecha_pago') 
    
    # Si hay fechas de filtro, aplicamos el mismo filtro en la consulta 'reporte'
    if fecha_inicio and fecha_fin:
        reporte = reporte.filter(fecha_pago__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        reporte = reporte.filter(fecha_pago__gte=fecha_inicio)
    elif fecha_fin:
        reporte = reporte.filter(fecha_pago__lte=fecha_fin)
    
    if nombre_obra:
        reporte = reporte.filter(reserva__funcion__obra__nombre__icontains=nombre_obra)
    
    total_ventas = resultados.aggregate(Sum('monto_total'))['monto_total__sum'] or 0

    # Si la acción es "descargar_pdf", generar y devolver el PDF
    if accion == 'descargar_pdf':
        administrador = request.user
        fecha_actual = datetime.now()
        context = {
            'now': fecha_actual,
            'administrador': administrador,
            'resultados': reporte,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_ventas': total_ventas
        }
    
        html_string = render_to_string('reporte_ventasPDF.html', context)
        pdf = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="reporte_ventas_{fecha_inicio}_{fecha_fin}.pdf"'

        return response
    
    data = {
        'resultados': reporte,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total_ventas': total_ventas
    }
    return render(request, 'reporte_ventas.html', data)

