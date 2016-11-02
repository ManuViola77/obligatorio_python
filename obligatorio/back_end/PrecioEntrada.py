from django.db import models
from back_end.Evento import Evento
from back_end.Sector import Sector

class PrecioEntrada(models.Model):
    precio = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    Evento = models.ForeignKey(Evento)
    Sector = models.ForeignKey(Sector)