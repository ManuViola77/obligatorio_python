from django.db import models
from back_end.Categoria import Categoria
from back_end.Lugar import Lugar

class Evento(models.Model):
    codigo = models.CharField(max_length = 4, unique = True)
    nombre = models.CharField(max_length = 50)
    descripcion = models.CharField(max_length = 100, null = True)
    fecha = models.DateTimeField()
    detalle = models.CharField(max_length = 50)
    afiche = models.ImageField()
    Categoria = models.ForeignKey(Categoria)
    Lugar = models.ForeignKey(Lugar)