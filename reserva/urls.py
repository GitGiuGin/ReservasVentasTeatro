from django.urls import path
from .views import confirmarFormReserva, nuevaReserva, confEditarReserva, editarReserva, cancelar_reserva

urlpatterns = [
    path('register/', nuevaReserva, name='reserva_nuevo'),
    path('confirmarReserva/funcion<int:funcion_id>', confirmarFormReserva, name='confirmar_reserva'),
    path('edit/<int:reserva_id>', confEditarReserva, name='reserva_editar'),
    path('reservaEditada/<int:reserva_id>', editarReserva, name='reserva_editada'),
    path('delete/<int:reserva_id>', cancelar_reserva, name='cancelar_reserva'),
]