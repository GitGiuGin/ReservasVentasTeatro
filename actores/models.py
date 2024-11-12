from django.db import models

# Create your models here.
class Actores (models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre del actor")
    apellido = models.CharField(max_length=50, verbose_name="Apellido del actor")
    edad = models.IntegerField(verbose_name="Edad del actor")

    class Meta:
        verbose_name = ("Actor")
        verbose_name_plural = ("Actores")
        db_table = 'actor'

    def __str__(self):
        return self.name

