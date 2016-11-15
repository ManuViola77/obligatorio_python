from django.db import models

class Pin(models.Model):
    valor = models.CharField(max_length = 4, null = True, unique = True)
    Telefono = models.OneToOneField("Telefono",on_delete = models.CASCADE,null = True)
    
    # si esta definido lo utiliza Django para el backend y templates 
    # evito urls hardcoded en el template
    def get_absoute_url(self):
        return "/portal/telefono/"
    
    def generatePin(self):
        from random import randint #python
        self.valor = str(randint(0000,9999))
        
    #redefino save del padre
    def save(self, *args, **kargs):
        self.generatePin()
        super(Pin,self).save(*args, **kargs)