from django.urls import path
from .views import *

urlpatterns = [
    path('pago/<int:reserva_id>', registrar_pago, name='registrar_pago'),
]