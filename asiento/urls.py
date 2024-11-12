from django.urls import path
from .views import *

urlpatterns = [
    path('reserve/<int:funcion_id>', formSelectAsiento, name='seleccion_asiento'),
    path('edit/<int:reserva_id>/funcion/<int:funcion_id>/', formEditAsiento, name='editar_asiento'),
]