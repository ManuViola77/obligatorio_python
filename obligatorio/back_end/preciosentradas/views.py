from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator,InvalidPage,PageNotAnInteger

# Create your views here.

from back_end.Lugar import Lugar

def index(request):
    #instancio Template
    template = loader.get_template('lugares/templates/index.html')
    usuario = request.GET.get("usuario")
    buscar = request.GET.get("buscar") # buscar = nombre del campo que quiero o del parametro de url
    pagina = request.GET.get("pagina")
    messages = get_messages(request)
    render = {}
    lugares = Lugar.objects.all()
    
    error = False
    if not pagina:
        pagina = 1
        
    if buscar is not None:
        lugares = lugares.filter(nombre__icontains=buscar)
    try:
        #Query set y cantidad de registros por pagina
        lugares = lugares.order_by('nombre','codigo') #'-nombre' para descendente
        paginator = Paginator(lugares,10)
        #paginado
        lugares = paginator.page(int(pagina))
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
    render['rows'] = lugares
    render['buscar'] = buscar
    render['pagina'] = pagina
    render['messages'] = messages
    # template tiene parametro {} diccionario de parametros que envio para el template
    return HttpResponse(template.render(render,request))

def save(request,id = None):   
    template    = loader.get_template('lugares/templates/save.html') 
    render      = {} #diccionario para pasar a la vista
    L           = Lugar() #instancio Lugar
    try:
        if id:#Update
            try:
                L = Lugar.objects.get(pk=id)
            except Lugar.DoesNotExist:
                messages.error(request,'Identificador no valido')
                return redirect('/lugares')
        #si postean form
        do_submit = request.POST.get("do_submit")
        if do_submit:
            for key,value in request.POST.items():
                if hasattr(L, key):
                    setattr(L, key, value)            
            
            required = ['codigo','nombre']
            for r in required:
                if not getattr(L, r):
                    raise Exception("Se deben ingresar los campos Codigo y Nombre.")
            
            #valido por ej que no exista codigo
            try:
                L2 = Lugar.objects.get(codigo=L.codigo)
                if id:
                    if L2 != L:
                        raise Exception("Codigo de Lugar {} ya existe ({})".format(L.codigo,L.nombre))
                else:
                    raise Exception("Codigo de Lugar {} ya existe ({})".format(L.codigo,L2.nombre))
                
            except Lugar.DoesNotExist:
                pass
            L.save()
            
            if not id:
                L = None
            render['success'] = "El lugar se ha {} correctamente...".format('actualizado' if id else 'ingresado')  
            
            
    except Exception as e:
        #Si "algo" me lanza una exception, lo muestro en el template
        render['error'] = e
    #render["id"] = id
    render["L"] = L
    return HttpResponse(template.render(render,request))


def delete(request,id):
    error = False
    msg   = ''
    if not id:
        error = True
        msg   = "Identificador no valido"
    else:
        try:
            L = Lugar.objects.get(pk = id)
        except Lugar.DoesNotExist:
            error = True
            msg   = "Identificador no valido"
    if not error:       
        L.delete()
        messages.success(request,"El Lugar se ha eliminado correctamente...")
    else:
        messages.error(request,msg)
    return redirect("/lugares")

