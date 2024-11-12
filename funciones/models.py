from django.db import models
from obra.models import Obra

# Create your models here.
class Funcion(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name="funciones", verbose_name="obra", null=True, blank=True)
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    hora = models.TimeField(verbose_name="Hora de la obra")

    class Meta:
        verbose_name = "Funcion"
        verbose_name_plural = "Funciones"
        db_table = 'funcion'

    def __str__(self):
        return self.name
    
    def formato_hora(self):
        if self.hora:
            return self.hora.strftime('%H:%M')  # Formato HH:MM
        return None
    
    def fecha_formateada(self):
        return self.fecha.strftime("%d/%m/%Y")
