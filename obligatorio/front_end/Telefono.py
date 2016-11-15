from django.db import models
from rest_framework import serializers

class Telefono(models.Model):
    numero = models.CharField(max_length = 11, null = True, unique = True)
    saldo = models.DecimalField(max_digits = 6,decimal_places = 2,default = 0)
    
class TelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefono
        fields = ('numero','saldo')