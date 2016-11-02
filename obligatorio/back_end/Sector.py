from django.db import models
from back_end.Lugar import Lugar

class Sector(models.Model):
    codigo = models.CharField(max_length = 4)
    nombre = models.CharField(max_length = 50)
    Lugar = models.ForeignKey(Lugar)
    
    class Meta:
        unique_together = ('codigo', 'Lugar',)