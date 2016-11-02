from django.db import models

class Categoria(models.Model):
    codigo = models.CharField(max_length = 4, unique = True)
    nombre = models.CharField(max_length = 50)