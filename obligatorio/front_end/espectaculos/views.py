from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator,InvalidPage,PageNotAnInteger

# Create your views here.

from back_end.Categoria import Categoria
from back_end.Evento import Evento
from back_end.Entrada import Entrada
from back_end.Asiento import Asiento
from back_end.Afiche import Afiche
from back_end.Sector import Sector
from datetime import datetime
import decimal
from back_end.PrecioEntrada import PrecioEntrada

def cantAsientosDisponibles(evento, sector):
    asientosSector      = Asiento.objects.filter(Sector = sector)
    entradasVendidas    = Entrada.objects.filter(Evento = evento)
    
    cant = 0    
    for A in asientosSector:
        x = entradasVendidas.filter(Asiento = A)
        if x.count() == 0:
            cant += 1
        
    return cant


def index(request):
    #instancio Template
    template    = loader.get_template('espectaculos/templates/index.html')
    usuario     = request.GET.get("usuario")
    buscar      = request.GET.get("buscar") # buscar = nombre del campo que quiero o del parametro de url
    catId       = request.GET.get("catBuscar")    
    pagina      = request.GET.get("pagina")
    messages    = get_messages(request)
    render      = {}

    categorias  = Categoria.objects.all()
    eventos     = Evento.objects.all()

    if catId is not None and catId != "0" :
        catId   = decimal.Decimal(catId)
        eventos = eventos.filter(Categoria__id = catId)
    
    hoy = datetime.today().date()
    eventos = eventos.filter(fecha__gte = hoy)

    if buscar is not None:
        eventos = eventos.filter(nombre__icontains=buscar)
        
    error = False
    if not pagina:
        pagina = 1
        
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
    
    render['error']      = error
    render['usuario']    = usuario
    render['categorias'] = categorias
    render['catSel']     = catId
    render['rows']       = eventos
    render['buscar']     = buscar
    render['pagina']     = pagina
    render['messages']   = messages
    
    # template tiene parametro {} diccionario de parametros que envio para el template
    return HttpResponse(template.render(render,request))




def detalle(request, id = None):   
    template    = loader.get_template('espectaculos/templates/detalle.html')
    render      = {} #diccionario para pasar a la vista
    
    if id is None:
        messages.error(request,'Identificador no valido')
        return redirect('/portal/espectaculos/')
                    
    try:
        E = Evento.objects.get(pk=id)
    except Evento.DoesNotExist:
        messages.error(request,'Identificador no valido')
        return redirect('/portal/espectaculos/')
    
    # Entradas Vendidas
    entradas = Entrada.objects.filter(Evento = E)
    entradas = entradas.count()
    
    # Entradas Restantes = asientos - vendidas
    asientos  = Asiento.objects.filter(Sector__Lugar = E.Lugar)
    asientos  = asientos.count()
    restantes = asientos - entradas
    
    # Mensaje de disponibilidad
    if asientos == 0 or restantes == 0:
        render["error"] = 'Entradas agotadas'
    else:
        disponibilidad = restantes * 100 / asientos        
        if disponibilidad > 50:
            render["mayor50"] = 'La disponibilidad es mayor al 50%'
        elif disponibilidad >= 10:
            render["entre10_50"] = 'La disponibilidad esta entre un 10% y un 50%'
        else:
            render["menor10"] = 'La disponibilidad es menor al 10%'        
    
    render["L"]         = E
    render["vendidas"]  = entradas
    render["restantes"] = restantes
        
    return HttpResponse(template.render(render,request))

def afiche(request, id):
    template    = loader.get_template('espectaculos/templates/afiche.html') 
    render      = {} #diccionario para pasar a la vista
    if not id:
        messages.error(request,'Identificador no valido')
        return redirect('/portal/espectaculos')
    else:
        try:
            E = Evento.objects.get(pk=id)
            if E.Afiche: 
                try:
                    A = Afiche.objects.get(pk = E.Afiche.id)     
                    render["A"] = A
                except Afiche.DoesNotExist:
                    raise Exception ("Afiche no existe")
            
            sectoresConPrecios = []
            sectores = Sector.objects.filter(Lugar = E.Lugar)
            for sector in sectores:
                cantDisponibles = cantAsientosDisponibles(E,sector)
                precioSector = PrecioEntrada.objects.filter(Evento = E, Sector = sector)
                precio = 0
                for precioS in precioSector:
                    precio = precioS.precio
                if precio > 0:
                    sectoresConPrecios.append({'sector':sector.nombre,'disponibles':str(cantDisponibles),'precio':precio})
        except Evento.DoesNotExist:
            messages.error(request,'Identificador no valido')
            return redirect('/back_end/eventos')
        render["E"] = E
        render["sectores"] = sectoresConPrecios
        
        return HttpResponse(template.render(render,request))