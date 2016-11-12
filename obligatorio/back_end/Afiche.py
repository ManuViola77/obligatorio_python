from django.db import models
from django.forms import ModelForm 

class Afiche(models.Model):
    archivo = models.ImageField(upload_to="afiches",null = True)
    
class AficheForm(ModelForm):
    
    class Meta:
        model = Afiche
        fields = ["archivo"]