from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator,InvalidPage,PageNotAnInteger

# Create your views here.

from back_end.Evento import Evento
from back_end.Asiento import Asiento
from back_end.Entrada import Entrada

def index(request,evento):
    #instancio Template
    template = loader.get_template('entradas/templates/index.html')
    usuario = request.GET.get("usuario")
    buscar = request.GET.get("buscar") # buscar = nombre del campo que quiero o del parametro de url
    pagina = request.GET.get("pagina")
    message = get_messages(request)
    render = {}
    
    if not evento:
        error = True
        messages.error(request,"Debe tener un evento asociado.")
    else: 
        eventoEntrada = Evento.objects.get(pk = evento)
        entradas = Entrada.objects.all()
        entradas = entradas.filter(Evento = eventoEntrada)
        if entradas:
            error = False
            if not pagina:
                pagina = 1
                
            if buscar is not None:
                entradas = entradas.filter(Asiento__Sector__nombre__icontains=buscar)
            try:
                #Query set y cantidad de registros por pagina
                entradas = entradas.order_by('Asiento__Sector__nombre','Asiento__numero') #'-nombre' para descendente
                paginator = Paginator(entradas,10)
                #paginado
                entradas = paginator.page(int(pagina))
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
            messages.error(request,"{} no tiene ninguna entrada asociada.".format(eventoEntrada.nombre)) 
            
    render['error'] = error
    render['usuario'] = usuario
    render['rows'] = entradas
    render['buscar'] = buscar
    render['pagina'] = pagina
    render['messages'] = message
    render['evento'] = eventoEntrada
    # template tiene parametro {} diccionario de parametros que envio para el template
    return HttpResponse(template.render(render,request))

def save(request,evento,id = None):   
    template    = loader.get_template('entradas/templates/save.html') 
    render      = {} #diccionario para pasar a la vista
    E           = Entrada() #instancio entrada
    if not evento:
        error = True
        messages.error(request,"Debe tener un evento asociado.")
    else: 
        try:
            if id:#Update
                try:
                    E = Entrada.objects.get(pk=id)
                except Entrada.DoesNotExist:
                    messages.error(request,'Identificador no valido')
                    return redirect('/back_end/entradas/'+evento)
            else:
                E = Entrada()
        except Exception as e:
            #Si "algo" me lanza una exception, lo muestro en el template
            render['error'] = e
                    
        eventoEntrada  = Evento.objects.get(pk = evento) #instancio Evento
        asientos = Asiento.objects.filter(Sector__LugarSector = eventoEntrada.Lugar)
        entradasVendidas = Entrada.objects.filter(Asiento__Sector__LugarSector = eventoEntrada.Lugar)
        for ent in entradasVendidas:
            if not id:
                asientos = asientos.exclude(pk=ent.Asiento.id)
            else:
                if ent.Asiento.id != E.Asiento.id:
                    asientos = asientos.exclude(pk=ent.Asiento.id)
            
        asientos = asientos.order_by('Sector__nombre','numero')
        if not asientos: 
            messages.error(request,"El lugar del evento no tiene asientos asignados.")
            return redirect('/back_end/entradas/'+evento)
        
        try:
            if id:#Update
                try:
                    E = Entrada.objects.get(pk=id)
                except Entrada.DoesNotExist:
                    messages.error(request,'Identificador no valido')
                    return redirect('/back_end/entradas/'+evento)
            #si postean form
            do_submit = request.POST.get("do_submit")
            if do_submit:
                
                for key,value in request.POST.items():
                    if hasattr(E, key):
                        setattr(E, key, value)            
                
                #grabo asiento
                if request.POST.get("asiento"):
                    #programacion defensiva (validar que exista pk)
                    asientoEntrada = Asiento.objects.get(pk=request.POST.get("asiento"))
                    E.Asiento = asientoEntrada
                else:
                    raise Exception("Se debe ingresar Asiento.")

                
                #valido por ej que no exista Asiento
                try:
                    E2 = Entrada.objects.get(Asiento=E.Asiento)
                    if id:
                        if E2 != E:
                            raise Exception("Ya existe entrada para el Asiento {}".format(E.Asiento.numero))
                    else:
                        raise Exception("Ya existe entrada para el Asiento {}".format(E.Asiento.numero))
                    
                except Entrada.DoesNotExist:
                    pass
                
                E.Evento = eventoEntrada
                E.save()
                
                if not id:
                    E = None
                render['success'] = "El Entrada se ha {} correctamente...".format('actualizado' if id else 'ingresado')  
                
                
        except Exception as e:
            #Si "algo" me lanza una exception, lo muestro en el template
            render['error'] = e
    #render["id"] = id
    render["E"] = E
    render["evento"] = eventoEntrada
    render["asientos"] = asientos
    return HttpResponse(template.render(render,request))


def delete(request,evento,id):
    error = False
    msg   = ''
    if not id:
        error = True
        msg   = "Identificador no valido"
    else:
        try:
            E = Entrada.objects.get(pk = id)
        except Entrada.DoesNotExist:
            error = True
            msg   = "Identificador no valido"
    if not error:       
        E.delete()
        messages.success(request,"La Entrada se ha eliminado correctamente...")
    else:
        messages.error(request,msg)
    return redirect("/back_end/entradas/"+evento)

