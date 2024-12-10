from django.urls import path
from .views import vista_preliminar_reporte_clientes, descargar_reporte_pdf, reporte_ventas

urlpatterns = [
    path('clientes/', vista_preliminar_reporte_clientes, name='reporte_clientes'),
    path('clientes/descargar/', descargar_reporte_pdf, name='descargar_reporte_pdf'),
    path('ventas/', reporte_ventas, name='reporte_ventas'),
]