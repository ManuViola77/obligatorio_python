from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator,InvalidPage,PageNotAnInteger

# Create your views here.

from back_end.Lugar import Lugar
from back_end.Sector import Sector
from back_end.Asiento import Asiento

def index(request,lugar):
    #instancio Template
    template = loader.get_template('sectores/templates/index.html')
    usuario = request.GET.get("usuario")
    buscar = request.GET.get("buscar") # buscar = nombre del campo que quiero o del parametro de url
    pagina = request.GET.get("pagina")
    message = get_messages(request)
    render = {}
    cantAsientos = 0
    
    if not lugar:
        error = True
        messages.error(request,"Debe tener un lugar asociado.")
    else:     
        lugarSector = Lugar.objects.get(pk=lugar)
        sectores = Sector.objects.all()
        sectores = sectores.filter(LugarSector = lugarSector)
        if sectores: 
            error = False
            if not pagina:
                pagina = 1

            if buscar is not None:
                sectores = sectores.filter(nombre__icontains=buscar)
            try:
                #Query set y cantidad de registros por pagina
                sectores = sectores.order_by('nombre','codigo') #'-nombre' para descendente
                paginator = Paginator(sectores,10)
                #paginado
                sectores = paginator.page(int(pagina))
                cantAsientos = []
                for sector in sectores:
                    asientos = Asiento.objects.all()
                    asientosActual = asientos.filter(Sector = sector)
                    cantAsientosActual = asientosActual.count()
                    cantAsientos.append(cantAsientosActual)
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
            messages.error(request,"{} no tiene ningun sector asociado.".format(lugarSector.nombre))  
             
    render['error'] = error
    render['usuario'] = usuario
    render['rows'] = sectores
    render['lugar'] = lugarSector
    render['buscar'] = buscar
    render['pagina'] = pagina
    render['messages'] = message
    render['asientos'] = cantAsientos

    # template tiene parametro {} diccionario de parametros que envio para el template
    return HttpResponse(template.render(render,request))

def save(request,lugar,id = None):   
    template    = loader.get_template('sectores/templates/save.html') 
    render      = {} #diccionario para pasar a la vista
    cantAsientos = 0
    
    if not lugar:
        error = True
        messages.error(request,"Debe tener un lugar asociado.")
    else:    
        lugarSector  = Lugar.objects.get(pk = lugar) #instancio Lugar
        S = Sector()
        try:
            if id:#Update
                try:
                    S = Sector.objects.get(pk=id)
                    asientos = Asiento.objects.all()
                    asientosActual = asientos.filter(Sector = S)
                    cantAsientos = asientosActual.count()
                except Sector.DoesNotExist:
                    messages.error(request,'Identificador no valido')
                    return redirect('/back_end/lugares/'+lugar+'/sectores/')
            #si postean form
            do_submit = request.POST.get("do_submit")
            if do_submit:
                for key,value in request.POST.items():
                    if hasattr(S, key):
                        setattr(S, key, value)            
                
                required = ['codigo','nombre']
                for r in required:
                    if not getattr(S, r):
                        raise Exception("Se deben ingresar los campos Codigo y Nombre.")
                
                if request.POST.get("asientos"):
                    try:
                        cantAsientos = int(request.POST.get("asientos"))
                    except ValueError:
                        raise Exception("Cantidad de Asientos no es un numero")
                #valido por ej que no exista codigo
                try:
                    S2 = Sector.objects.get(codigo=S.codigo,LugarSector = lugarSector)
                    if id:
                        if S2 != S:
                            raise Exception("Codigo de Sector {} para el lugar {} ya existe ({})".format(S.codigo,lugarSector.nombre,S2.nombre))
                    else:
                        raise Exception("Codigo de Sector {} para el lugar {} ya existe ({})".format(S.codigo,lugarSector.nombre,S2.nombre))
                    
                except Sector.DoesNotExist:
                    pass
                S.LugarSector = lugarSector
                S.save()
                
                asientos = Asiento.objects.all()
                asientosActual = asientos.filter(Sector = S)
                cantAsientosActual = asientosActual.count()
                if cantAsientos: 
                    if cantAsientosActual > cantAsientos:
                        asientosActual = asientosActual.order_by('-numero')
                        for asiento in asientosActual:
                            if cantAsientosActual > cantAsientos:
                                asiento.delete()
                                cantAsientosActual -=1
                            else:
                                break
                    if cantAsientosActual < cantAsientos:    
                        for x in range(cantAsientosActual+1, cantAsientos+1):
                            A = Asiento()
                            A.numero = x
                            A.Sector = S
                            A.save()
                
                if not id:
                    S = None
                    cantAsientos = None
                render['success'] = "El sector se ha {} correctamente...".format('actualizado' if id else 'ingresado')  
                
                
        except Exception as e:
            #Si "algo" me lanza una exception, lo muestro en el template
            render['error'] = e
    #render["id"] = id
    render["S"] = S
    render["lugar"] = lugarSector
    render["asientos"] = cantAsientos
    return HttpResponse(template.render(render,request))


def delete(request,lugar,id):
    error = False
    msg   = ''
    if not id:
        error = True
        msg   = "Identificador no valido"
    else:
        try:
            S = Sector.objects.get(pk = id)
        except Sector.DoesNotExist:
            error = True
            msg   = "Identificador no valido"
    if not error:       
        S.delete()
        messages.success(request,"El Sector se ha eliminado correctamente...")
    else:
        messages.error(request,msg)
    return redirect("/back_end/lugares/"+lugar+"/sectores/")

