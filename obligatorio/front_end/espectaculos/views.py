from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator,InvalidPage,PageNotAnInteger

# Create your views here.

from back_end.Evento import Evento
from datetime import datetime

def index(request, id = None):
    #instancio Template
    template = loader.get_template('espectaculos/templates/index.html')
    usuario = request.GET.get("usuario")
    buscar = request.GET.get("buscar") # buscar = nombre del campo que quiero o del parametro de url
    pagina = request.GET.get("pagina")
    messages = get_messages(request)
    render = {}

    eventos = Evento.objects.all()

    if id is not None:
        eventos = eventos.filter(Categoria__id = id)
    
    hoy = datetime.today()
#    eventos = eventos.filter(Evento.fecha >= hoy)
        
    error = False
    if not pagina:
        pagina = 1
        
    if buscar is not None:
        eventos = eventos.filter(nombre__icontains=buscar)
    try:
        #Query set y cantidad de registros por pagina
        eventos = eventos.order_by('fecha','nombre') #'-nombre' para descendente
        paginator = Paginator(eventos,10)
        #paginado
        eventos = paginator.page(int(pagina))
    except InvalidPage:
            error = True
            messages.error(request,"Numero de pagina no valida")
    except ValueError:
            error = True
            messages.error(request,"Numero de pagina no valida")
    except PageNotAnInteger:
            error = True
            messages.error(request,"Numero de pagina no valida")
    
    render['error'] = error
    render['usuario'] = usuario
    render['rows'] = eventos
    render['buscar'] = buscar
    render['pagina'] = pagina
    render['messages'] = messages
    # template tiene parametro {} diccionario de parametros que envio para el template
    return HttpResponse(template.render(render,request))




def detalle(request, id = None):   
    template    = loader.get_template('espectaculos/templates/detalle.html') 
    render      = {} #diccionario para pasar a la vista
    
    if id is None:
        messages.error(request,'Identificador no valido')
        return redirect('/portal/index')
                    
    try:
        E = Evento.objects.get(pk=id)
    except Evento.DoesNotExist:
        messages.error(request,'Identificador no valido')
        return redirect('/portal/index')
                
    render["L"] = E
    return HttpResponse(template.render(render,request))

