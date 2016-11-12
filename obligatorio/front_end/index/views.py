from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator,InvalidPage,PageNotAnInteger

# Create your views here.

from back_end.Categoria import Categoria

def index(request):
    #instancio Template
    template = loader.get_template('index/templates/index.html')
    usuario = request.GET.get("usuario")
    buscar = request.GET.get("buscar") # buscar = nombre del campo que quiero o del parametro de url
    pagina = request.GET.get("pagina")
    messages = get_messages(request)
    render = {}
    categorias = Categoria.objects.all()
    
    error = False
    if not pagina:
        pagina = 1
        
    if buscar is not None:
        categorias = categorias.filter(nombre__icontains=buscar)
    try:
        #Query set y cantidad de registros por pagina
        categorias = categorias.order_by('nombre','codigo') #'-nombre' para descendente
        paginator = Paginator(categorias,10)
        #paginado
        categorias = paginator.page(int(pagina))
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
    render['rows'] = categorias
    render['buscar'] = buscar
    render['pagina'] = pagina
    render['messages'] = messages
    # template tiene parametro {} diccionario de parametros que envio para el template
    return HttpResponse(template.render(render,request))

