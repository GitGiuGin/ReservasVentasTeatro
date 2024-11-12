from django.db import models

# Create your models here.
class Asiento(models.Model):
    numero_asiento = models.CharField(max_length=5, verbose_name="Número de asiento")

    class Meta:
        verbose_name = "Asiento"
        verbose_name_plural = "Asientos"
        db_table = 'asiento'

    def __str__(self):
        return f"{self.numero_asiento}"
