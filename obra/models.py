from django.db import models
from actores.models import Actores

# Create your models here.
class Obra(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre de la obra")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='obras/', null=True, blank=True, verbose_name="Imagen de la obra")
    estado = models.BooleanField(default=True)
    # Relación Many-to-Many con el modelo Actores
    actores = models.ManyToManyField(Actores, related_name="obras", verbose_name="Actores en la obra", blank=True)


    class Meta:
        verbose_name = "Obra"
        verbose_name_plural = "Obras"
        db_table = 'obra'

    def __str__(self):
        return self.nombre
    
    def precio_bs(self):
        return f"{self.precio} Bs"
    
    @property
    def estado_display(self):
        return "Activo" if self.estado else "Inactivo"