from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator,InvalidPage,PageNotAnInteger

# Create your views here.

from back_end.Evento import Evento
from back_end.PrecioEntrada import PrecioEntrada
from back_end.Sector import Sector
from back_end.Lugar import Lugar


def index(request,evento):
    #instancio Template
    template = loader.get_template('preciosentradas/templates/index.html')
    usuario = request.GET.get("usuario")
    buscar = request.GET.get("buscar") # buscar = nombre del campo que quiero o del parametro de url
    pagina = request.GET.get("pagina")
    message = get_messages(request)
    render = {}
    
    if not evento:
        error = True
        messages.error(request,"Debe tener un evento asociado.")
    else: 
        eventoPrecioEntrada = Evento.objects.get(pk = evento)
        precioEntrada = PrecioEntrada.objects.all()
        precioEntrada = precioEntrada.filter(Evento = eventoPrecioEntrada)
        if precioEntrada:
            error = False
            if not pagina:
                pagina = 1
                
            if buscar is not None:
                precioEntrada = precioEntrada.filter(Sector__nombre__icontains=buscar)
            try:
                #Query set y cantidad de registros por pagina
                precioEntrada = precioEntrada.order_by('precio','Sector__nombre') #'-nombre' para descendente
                paginator = Paginator(precioEntrada,10)
                #paginado
                precioEntrada = paginator.page(int(pagina))
            except InvalidPage:
                    error = True
                    messages.error(request,"Numero de pagina no valida")
            except ValueError:
                    error = True
                    messages.error(request,"Numero de pagina no valida")
            except PageNotAnInteger:
                    error = True
                    messages.error(request,"Numero de pagina no valida")
        else:
            error = True
            messages.error(request,"{} no tiene ningun precio de entrada asociado.".format(eventoPrecioEntrada.nombre)) 
            
    render['error'] = error
    render['usuario'] = usuario
    render['rows'] = precioEntrada
    render['buscar'] = buscar
    render['pagina'] = pagina
    render['messages'] = message
    render['evento'] = eventoPrecioEntrada
    # template tiene parametro {} diccionario de parametros que envio para el template
    return HttpResponse(template.render(render,request))

def save(request,evento,id = None):   
    template    = loader.get_template('preciosentradas/templates/save.html') 
    render      = {} #diccionario para pasar a la vista
    PE           = PrecioEntrada() #instancio entrada
    if not evento:
        error = True
        messages.error(request,"Debe tener un evento asociado.")
    else: 
        try:
            if id:#Update
                try:
                    PE = PrecioEntrada.objects.get(pk=id)
                except PrecioEntrada.DoesNotExist:
                    messages.error(request,'Identificador no valido')
                    return redirect('/back_end/preciosentradas/'+evento)
            else:
                PE = PrecioEntrada()
        except Exception as e:
            #Si "algo" me lanza una exception, lo muestro en el template
            render['error'] = e
            
        eventoPrecioEntrada  = Evento.objects.get(pk = evento) #instancio Evento
        sectores = Sector.objects.filter(LugarSector = eventoPrecioEntrada.Lugar)
        preciosEntradasYaIngresados = PrecioEntrada.objects.filter(Sector__LugarSector = eventoPrecioEntrada.Lugar)
        for precioIngresado in preciosEntradasYaIngresados:
            if not id:
                sectores = sectores.exclude(pk= precioIngresado.Sector.id)
            else:
                if precioIngresado.Sector.id != PE.Sector.id:
                    sectores = sectores.exclude(pk= precioIngresado.Sector.id)
                
        sectores = sectores.order_by('nombre')
        if not sectores: 
            messages.error(request,"El lugar del evento no tiene sectores o ya todos tienen precio de entrada asignado.")
            return redirect('/back_end/preciosentradas/'+evento)
        
        try:
            #si postean form
            do_submit = request.POST.get("do_submit")
            if do_submit:
                
                for key,value in request.POST.items():
                    if hasattr(PE, key):
                        setattr(PE, key, value)            
                
                #grabo sector
                if request.POST.get("sector"):
                    #programacion defensiva (validar que exista pk)
                    sectorPrecioEntrada = Sector.objects.get(pk=request.POST.get("sector"))
                    PE.Sector = sectorPrecioEntrada
                else:
                    raise Exception("Se debe ingresar Sector.")

                
                #valido que no exista Sector
                try:
                    PE2 = PrecioEntrada.objects.get(Sector=PE.Sector)
                    if id:
                        if PE2 != PE:
                            raise Exception("Ya existe Precio de Entrada para el Sector {}".format(PE.Sector.nombre))
                    else:
                        raise Exception("Ya existe entrada para el Sector {}".format(PE.Sector.nombre))
                    
                except PrecioEntrada.DoesNotExist:
                    pass
                
                PE.Evento = eventoPrecioEntrada
                PE.save()
                
                if not id:
                    PE = None
                render['success'] = "El Precio de Entrada se ha {} correctamente...".format('actualizado' if id else 'ingresado')  
                
                
        except Exception as e:
            #Si "algo" me lanza una exception, lo muestro en el template
            render['error'] = e
    #render["id"] = id
    render["PE"] = PE
    render["evento"] = eventoPrecioEntrada
    render["sectores"] = sectores
    return HttpResponse(template.render(render,request))


def delete(request,evento,id):
    error = False
    msg   = ''
    if not id:
        error = True
        msg   = "Identificador no valido"
    else:
        try:
            PE = PrecioEntrada.objects.get(pk = id)
        except PrecioEntrada.DoesNotExist:
            error = True
            msg   = "Identificador no valido"
    if not error:       
        PE.delete()
        messages.success(request,"El Precio de Entrada se ha eliminado correctamente...")
    else:
        messages.error(request,msg)
    return redirect("/back_end/preciosentradas/"+evento)

