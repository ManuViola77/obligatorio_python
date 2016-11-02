from django.db import models
from back_end.Sector import Sector

class Asiento(models.Model):
    numero = models.IntegerField()
    Sector = models.ForeignKey(Sector)
    
    class Meta:
        unique_together = ('numero', 'Sector',)