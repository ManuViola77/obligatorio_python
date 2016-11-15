from django.db import models
from back_end.Categoria import Categoria
from back_end.Lugar import Lugar
from back_end.Afiche import Afiche
from datetime import datetime

class Evento(models.Model):
    codigo = models.CharField(max_length = 4, unique = True)
    nombre = models.CharField(max_length = 50)
    descripcion = models.CharField(max_length = 100, null = True)
    fecha = models.DateTimeField()
    detalle = models.CharField(max_length = 50)
    Afiche = models.ForeignKey(Afiche, null = True)
    Categoria = models.ForeignKey(Categoria)
    Lugar = models.ForeignKey(Lugar)
    
    def diasInicio(self):
        hoy = datetime.today().date()
        td = self.fecha.date()- hoy
        dias = td.days
        if dias > 0:
            return dias
        else:
            return 0
        
    """def cantAsientosDisponibles(self, sector):
        asientosSector      = Asiento.objects.filter(Sector = sector)
        entradasVendidas    = Entrada.objects.filter(Evento = self)
        
        cant = 0    
        for A in asientosSector:
            x = entradasVendidas.filter(Asiento = A)
            if x.count() == 0:
                cant += 1
            
        return cant
    
    
    def getAsientoDisponible(self, sector):         
        asientosSector      = Asiento.objects.filter(Sector = sector)
        entradasVendidas    = Entrada.objects.filter(Evento = self)
        for A in asientosSector:
            x = entradasVendidas.filter(Asiento = A)
            if x.count() == 0:
                return A
    """    
        