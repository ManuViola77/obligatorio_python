from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator,InvalidPage,PageNotAnInteger
from rest_framework.decorators import api_view
import decimal
from rest_framework.response import Response
from rest_framework import status
import urllib2,json

# Create your views here.
from front_end.Telefono import Telefono, TelefonoSerializer
from front_end.Pin import Pin
from back_end.Evento import Evento
from back_end.Sector import Sector
from back_end.Asiento import Asiento
from back_end.Entrada import Entrada
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


def getAsientoDisponible(evento, sector):         
    asientosSector      = Asiento.objects.filter(Sector = sector)
    entradasVendidas    = Entrada.objects.filter(Evento = evento)
    for A in asientosSector:
        x = entradasVendidas.filter(Asiento = A)
        if x.count() == 0:
            return A
    
 
def registarEntrada(evento, sector, telefono):
    E           = Entrada()
    E.telefono  = telefono
    E.Evento    = evento
    E.Asiento   = getAsientoDisponible(evento, sector)
    E.save()
       


def telefono(request, idEvento=None):
    context = {}

    if not idEvento:
        messages.error(request,'Espectaculo no valido')
        return redirect('/portal/espectaculos/')
    else:
        try:
            E = Evento.objects.get(pk = idEvento)
        except Evento.DoesNotExist:
            messages.error(request,'Espectaculo no valido')
            return redirect('/portal/espectaculos/')
        
    sectores        = Sector.objects.filter(Lugar = E.Lugar)
    secId           = 0
    cantEntradas    = 0
        
    T = Telefono()
    P = Pin()
    try:
        if request.POST:
                                
            secId           = request.POST.get("sector")            
            cantEntradas    = request.POST.get("entradas")
            tel_numero      = request.POST.get("numero")
            T.numero        = tel_numero
            
            if not secId or secId == "0":
                raise Exception("Selecccione sector para continuar")
            try: 
                secId = decimal.Decimal(secId)
            except decimal.InvalidOperation:
                raise Exception ("Selecccione sector para continuar")
            
            if not cantEntradas:
                raise Exception("Ingrese cantidad de entradas para continuar")            
            try: 
                cantEntradas = decimal.Decimal(cantEntradas)
            except decimal.InvalidOperation:
                raise Exception ("Cantidad de entradas no valido")
            
            if not tel_numero:
                raise Exception("Ingrese telefono para continuar")
            
            sector = Sector.objects.get(pk=secId)
            x      = cantAsientosDisponibles(E, sector)
            if cantEntradas > x:
                raise Exception("El sector {} tiene {} asientos disponibles".format(sector.nombre, x))
            
            try:
                T = Telefono.objects.get(numero = tel_numero)
            except Telefono.DoesNotExist:
                T.save()            
            
            try:
                P = Pin.objects.get(Telefono = T)
            except Pin.DoesNotExist:
                P.Telefono = T            
            
            P.save()
            messages.success(request,"Su PIN es {}".format(P.valor))
            return redirect("/portal/telefono/validarpin/{}/{}/{}/".format(idEvento, secId, cantEntradas))
        
    except Exception as e:
        context['error'] = e
        
    context['T'] = T
    context['P'] = P
    context['sectores']     = sectores
    context['sectorId']     = decimal.Decimal(secId)
    context['cantEntradas'] = cantEntradas
    
    return render(request,"telefono/templates/telefono.html",context)


def validarpin(request,idEvento=None,secId=None,cantEntradas=None):
    
    if not idEvento:
        messages.error(request,'Espectaculo no valido')
        return redirect('/portal/espectaculos/')
    try: 
        idEvento = decimal.Decimal(idEvento)
    except decimal.InvalidOperation:
        messages.error(request,'Espectaculo no valido')
        return redirect('/portal/espectaculos/')    
    try:
        E = Evento.objects.get(pk = idEvento)
    except Evento.DoesNotExist:
        messages.error(request,'Espectaculo no valido')
        return redirect('/portal/espectaculos/')
    
    if not secId:
        messages.error(request,'Sector no valido')
        return redirect('/portal/espectaculos/')
    try: 
        secId = decimal.Decimal(secId)
    except decimal.InvalidOperation:
        messages.error(request,'Sector no valido')
        return redirect('/portal/espectaculos/')    
    try:
        sector = Sector.objects.get(pk = secId)
    except Sector.DoesNotExist:
        messages.error(request,'Sector no valido')
        return redirect('/portal/espectaculos/')
    
    if not cantEntradas:
        messages.error(request,'Cantidad de entradas no valido')
        return redirect('/portal/espectaculos/')
    try: 
        cantEntradas = decimal.Decimal(cantEntradas)
    except decimal.InvalidOperation:
        messages.error(request,'Cantidad de entradas no valido')
        return redirect('/portal/espectaculos/')    
    
    
    context = {}
    T = Telefono()
    P = Pin()
    try:
        if request.POST:
            
            P.valor = request.POST.get("pin")
            if not P.valor:
                raise Exception("Ingrese pin enviado para continuar")
            try:
                P = Pin.objects.get(valor = P.valor)
            except Pin.DoesNotExist:
                raise Exception("Numero de PIN invalido")
            
            # Precio de las entradas
            precioEntrada = PrecioEntrada.objects.filter(Evento = E).get(Sector = sector)
            precio = precioEntrada.precio * cantEntradas
            
            try:
                #GET Telefono para saldo actual                
                opener = urllib2.build_opener(urllib2.HTTPHandler)
                #no especifico metodo, por defecto es GET
                url = "http://localhost/portal/telefono/api/{}".format(P.Telefono.id)
                datos_tel = urllib2.urlopen(url).read()
                if datos_tel:
                    #convierto respuesta a diccionario
                    datos_tel = json.loads(datos_tel)                     

                saldoActual = datos_tel.get("saldo")
                saldoActual = decimal.Decimal(saldoActual)
                
                if saldoActual < precio:
                    raise Exception("No tiene saldo suficiente")
                
                saldo = saldoActual - precio

                #PUT: actualizo saldo
                datos = json.dumps({"saldo":str(saldo)})
                #request con url y datos formato JSON
                enviar = urllib2.Request(url, data = datos)
                #le aviso a server que le estoy enviando JSON
                enviar.add_header('Content-Type','application/json')
                #especifico metodo
                enviar.get_method = lambda: 'PUT'
                #ejecuto request
                response = opener.open(enviar)
                # REST put siempre devuelve datos modificados
                datos_put = response.read()
                datos_put = json.loads(datos_put)
                                                
            except urllib2.HTTPError as e:
                #por ejemplo server me retorno HTTP Code 404
                if e.code == 404:
                    raise Exception("No se encontro el recurso")
                else:
                    raise Exception(e.read(),e.code)
            
            
            # Registro entradas
            for i in range (cantEntradas):
                print i
                registarEntrada(E, sector, P.Telefono.numero)
                            
            # Borro pin
            P.delete()
                            
            msg = "Se ha finalizado tu compra, retira tus entradas con el numero de documento {} en {} el dia {}".format("[DOC]", E.Lugar.nombre, E.fecha.date()) 
            messages.success(request, msg)
            return redirect("/portal/espectaculos/")
            
    except Exception as e:
        context["error"] = e
    
    
    context['P']        = P
    context['idEvento'] = idEvento
    context['idSector'] = secId
    context['entradas'] = cantEntradas
    template            = loader.get_template('telefono/templates/enviarpin.html')
    return HttpResponse(template.render(context,request))


def recarga(request):
    context = {}  
    T = Telefono()
    do_submit = request.POST.get("do_submit")
    try:
        if do_submit:
            
            for key,value in request.POST.items():
                if hasattr(T, key):
                    setattr(T, key, value)
            if not T.numero:
                raise Exception("Ingrese telefono para continuar")
            if not T.saldo:
                raise Exception("Ingrese saldo para continuar")
            try: 
                T.saldo = decimal.Decimal(T.saldo)
            except decimal.InvalidOperation:
                raise Exception ("Saldo no valido")
            try:
                T2 = Telefono.objects.get(numero=T.numero)   
            except Telefono.DoesNotExist:
                raise Exception ("Telefono no existe")
            
            #PUT, GET a telefono            
            try:
                #GET para saldo actual
                opener = urllib2.build_opener(urllib2.HTTPHandler)
                #no especifico metodo, por defecto es GET
                url = "http://localhost/portal/telefono/api/{}".format(T2.id)                
                datos_tel = urllib2.urlopen(url).read()                
                if datos_tel: 
                    #convierto respuesta a diccionario
                    datos_tel = json.loads(datos_tel)
                
                saldoActual = datos_tel.get("saldo")
                saldoActual = decimal.Decimal(saldoActual)            
                saldo = saldoActual + T.saldo

                #PUT
                datos = json.dumps({"saldo":str(saldo)})
                #request con url y datos formato JSON
                enviar = urllib2.Request(url, data = datos)
                #le aviso a server que le estoy enviando JSON
                enviar.add_header('Content-Type','application/json')
                #especifico metodo
                enviar.get_method = lambda: 'PUT'
                #ejecuto request
                response = opener.open(enviar)
                # REST put siempre devuelve datos modificados
                datos_put = response.read()
                datos_put = json.loads(datos_put)
                context["success"] = "Saldo se ha actualizado correctamente, anterior {}, actual {}".format(datos_tel.get("saldo"),datos_put.get("saldo"))
                
            except urllib2.HTTPError as e:
                #por ejemplo server me retorno HTTP Code 404
                if e.code == 404:
                    raise Exception("No se encontro el recurso")
                else:
                    raise Exception(e.read(),e.code)
             
    except Exception as e:
        context["error"] = e
        
    context["T"] = T
        
    return render(request,"telefono/templates/recarga.html",context)

#api de telefono
@api_view(["GET","PUT"])
def telefono_api(request, pk = None):
    if request.method == "GET":
        if pk:
            try:
                T = Telefono.objects.get(pk=pk)
            except Telefono.DoesNotExist:
                return Response(status = status.HTTP_404_NOT_FOUND)
            serializer = TelefonoSerializer(T)
        else:
            telefonos = Telefono.objects.all()
            serializer = TelefonoSerializer(telefonos,many=True)
        return Response(serializer.data) #200 ok
        
    if request.method == "PUT":
        try:
            T = Telefono.objects.get(pk = pk)
        except Telefono.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)   
        serializer = TelefonoSerializer(T,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) #200 ok
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    