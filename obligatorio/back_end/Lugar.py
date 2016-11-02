from django.db import models

class Lugar(models.Model):
    codigo = models.CharField(max_length = 4, unique = True)
    nombre = models.CharField(max_length = 50)
    direccion = models.CharField(max_length = 50, null = True)
    telefono = models.CharField(max_length = 15, null = True)