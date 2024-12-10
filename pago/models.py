from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from reserva.models import Reserva
import os

def renombrar_archivo_pago(instance, filename):
    extension = os.path.splitext(filename)[1]  # Obtiene la extensión del archivo (.pdf)
    nombre_archivo = f"comprobante{instance.id or 'temp'}{extension}"
    return os.path.join('comprobantes/', nombre_archivo)

# Create your models here.
class Pago(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, verbose_name="Reserva")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Total")
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Pago")
    metodo_pago = models.CharField(max_length=50, verbose_name="Método de Pago")
    archivo_pago = models.FileField(upload_to='comprobantes/', null=True, blank=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        db_table = 'pago'

    def __str__(self):
        return f"Pago de {self.monto_total} para la reserva {self.reserva.id}"
    
@receiver(post_save, sender=Pago)
def renombrar_archivo_post_save(sender, instance, created, **kwargs):
    if created and instance.archivo_pago:
        # Obtiene la ruta actual y genera la nueva ruta
        archivo_actual = instance.archivo_pago.path
        nueva_ruta = os.path.join(
            os.path.dirname(archivo_actual),
            f"comprobante_{instance.id}{os.path.splitext(archivo_actual)[1]}"
        )
        # Renombra el archivo
        os.rename(archivo_actual, nueva_ruta)
        # Actualiza el campo en la base de datos
        instance.archivo_pago.name = os.path.relpath(nueva_ruta, 'comprobantes/')
        instance.save()