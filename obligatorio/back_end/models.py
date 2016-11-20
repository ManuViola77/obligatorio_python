from __future__ import unicode_literals

from django.db import models
from back_end.Lugar import Lugar
from back_end.Sector import Sector
from back_end.PrecioEntrada import PrecioEntrada
from back_end.Evento import Evento
from back_end.Categoria import Categoria
from back_end.Asiento import Asiento
from back_end.Entrada import Entrada
from back_end.Afiche import Afiche

# Create your models here.

from Lib.DAO.Dao import Dao
class Model(object):
    DAO         = None
    id          = None
    creado      = None
    actualizado = None
    
    def __init__(self):
        self.DAO = Dao()
    
    def load(self):
        return self.DAO.load(self)    
    
    def delete(self):
        self.DAO.delete(self)
        
    def save(self):
        if self.id:
            self.update()
        else:
            self.create()
    
    def create(self):
        self.DAO.create(self)
        
    def update(self):
        self.DAO.update(self)
        
    def fetchAll(self, Q = None):
        return self.DAO.fetchAll(self, Q)
    
    def fetch(self):
        return self.DAO.fetch(self)
    
    def objects(self):
        #Model.__class__
        return self.DAO.objects(self)
    
    def toArray(self):
        attributes = {}
        for key in dir(self):
            if not callable(getattr(self, key)) and not key.startswith('__') \
            and not isinstance(getattr(self, key), Dao):
                attributes[key] = getattr(self, key)
        return attributes
