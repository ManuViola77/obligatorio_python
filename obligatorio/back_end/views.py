from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

from back_end.Lugar import Lugar

def index(request):
    #instancio Template
    template = loader.get_template('templates/back_end/index.html')
    usuario = request.GET.get("usuario") # buscar = nombre del campo que quiero o del parametro de url
    # template tiene parametro {} diccionario de parametros que envio para el template
    return HttpResponse(template.render({'usuario':usuario},request))