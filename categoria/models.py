from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre de Categoria", default='Sin nombre', null=False)

    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")
        db_table = 'categoria'

    def __str__(self):
        return self.name

