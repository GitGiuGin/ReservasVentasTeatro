from django.db import models
from reserva.models import Reserva

# Create your models here.
class Pago(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, verbose_name="Reserva")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Total")
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Pago")
    metodo_pago = models.CharField(max_length=50, verbose_name="Método de Pago")

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        db_table = 'pago'

    def __str__(self):
        return f"Pago de {self.monto_total} para la reserva {self.reserva.id}"