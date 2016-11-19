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
from front_end.ProxyTelefono import ProxyTelefono



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
    
 
def registarEntrada(evento, sector, telefono, documento):
    E           = Entrada()
    E.telefono  = telefono
    E.documento = documento    
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
                raise Exception("Seleccione sector para continuar")
            try: 
                secId = decimal.Decimal(secId)
            except decimal.InvalidOperation:
                raise Exception ("Seleccione sector para continuar")
            
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
            importe = precioEntrada.precio * cantEntradas
                                    
            # Solicito compra al Servidor Externo
            numTel = P.Telefono.numero
            proxy = ProxyTelefono()
            documento = proxy.compra(numTel, importe) 
            
            # Registro entradas
            for i in range (cantEntradas):                
                registarEntrada(E, sector, numTel, documento)
                            
            # Borro pin
            P.delete()
                            
            msg = "Se ha finalizado tu compra, retira tus entradas con el numero de documento {} en {} el dia {}".format(documento, E.Lugar.nombre, E.fecha.date()) 
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
    numTel  = None
    importe = None    
    do_submit = request.POST.get("do_submit")
    try:
        if do_submit:
            numTel  = request.POST.get("numero")
            importe = request.POST.get("saldo")
                               
            if not numTel:
                raise Exception("Ingrese telefono para continuar")
            if not importe:
                raise Exception("Ingrese saldo para continuar")
            try: 
                importe = decimal.Decimal(importe)
            except decimal.InvalidOperation:
                raise Exception ("Saldo no valido")            

            proxy = ProxyTelefono()
            msg = proxy.recarga(numTel, importe)
            context["success"] = msg  
            
    except Exception as e:
        context["error"] = e
 
    context["numero"] = numTel
    context["saldo"]  = importe
    
    return render(request,"telefono/templates/recarga.html",context)

#api de telefono
@api_view(["GET","PUT"])
def telefono_api(request, numTel = None):
    if request.method == "GET":
        if numTel:
            try:
                T = Telefono.objects.get(numero = numTel)
            except Telefono.DoesNotExist:
                return Response(status = status.HTTP_404_NOT_FOUND)
            serializer = TelefonoSerializer(T)
        else:
            telefonos = Telefono.objects.all()
            serializer = TelefonoSerializer(telefonos,many=True)
        return Response(serializer.data) #200 ok
        
    if request.method == "PUT":
        try:
            T = Telefono.objects.get(numero = numTel)
        except Telefono.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)   
        serializer = TelefonoSerializer(T,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) #200 ok
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    