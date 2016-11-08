from django.db import models
from back_end.Evento import Evento
from back_end.Asiento import Asiento
from django.db.models.fields import NullBooleanField
from bson.json_util import default

class Entrada(models.Model):
    telefono = models.CharField(max_length = 11, null = True)
    documento = models.CharField(max_length = 11, null = True)
    usada = models.BooleanField(default = False)
    Evento = models.ForeignKey(Evento)
    Asiento = models.ForeignKey(Asiento,unique = True)