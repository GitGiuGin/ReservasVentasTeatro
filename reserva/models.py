from django.db import models
from funciones.models import Funcion
from asiento.models import Asiento
from usuario.models import Usuario

# Create your models here.
class Reserva(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Cliente")
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE, verbose_name="Funcion", blank=True, null=True)
    fecha_reserva = models.DateField(verbose_name="Fecha de la reserva", null=True, blank=True)
    estado = models.CharField(max_length=20, verbose_name="Estado reserva")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        db_table = 'reserva'

    def __str__(self):
        return f"Reserva de {self.cliente.usuario.username} para {self.obra.nombre}"

class ReservaAsiento(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='reservas_asientos')
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE, related_name='reservas_asientos')
    estado = models.BooleanField(default=True, verbose_name="Estado del Asiento en la Reserva")

    class Meta:
        verbose_name = "Reserva Asiento"
        verbose_name_plural = "Reservas Asientos"
        db_table = 'reserva_asiento'
        unique_together = ('reserva', 'asiento') 