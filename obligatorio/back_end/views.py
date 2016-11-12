from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator,InvalidPage,PageNotAnInteger
from demjson import JSON
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User

# Create your views here.

from back_end.Lugar import Lugar

def index(request):
    #instancio Template
    template = loader.get_template('templates/back_end/index.html')
    usuario = request.GET.get("usuario") # buscar = nombre del campo que quiero o del parametro de url
    # template tiene parametro {} diccionario de parametros que envio para el template
    return HttpResponse(template.render({'usuario':usuario},request))

def signin(request):
    context = {}
    message = get_messages(request)
    try:
        from django.contrib.auth import authenticate, login
        usr = pwd = ""
        if request.POST:
            usr = request.POST.get("usuario")
            pwd  = request.POST.get("password")
            if not usr or not pwd:
                raise Exception ("Ingrese Usuario y Password para continuar.")
            #autentico contra modelo usuario de django
            user = authenticate(username=usr,password=pwd)
            if user is not None:
                #dejo instancia de usuario en sesion
                login(request,user = user)
                return redirect("/back_end")
            else:
                raise Exception("Usuario o Password incorrecto")
    except Exception as e:
        context["error"] = e
        
    return render(request,"templates/back_end/login.html",context)    

def signout(request):   
    #elimino todo lo que esta en sesion
    logout(request)
    messages.success(request,"Su sesion ha finalizado")
    return redirect("/back_end/signin")

def registrar(request):
    context = {}
    message = get_messages(request)
    try:
        from django.contrib.auth import authenticate, login
        usr = pwd = ""
        if request.POST:
            usr = request.POST.get("usuario")
            pwd  = request.POST.get("password")
            if not usr or not pwd:
                raise Exception ("Ingrese Usuario y Password para continuar.")
            user = User.objects.create_user(username=usr,password=pwd)
            user.save()
            context['success'] = 'Usuario {} creado con exito'.format(usr)
            return redirect("/back_end/signin")

    except Exception as e:
        context["error"] = e
        
    return render(request,"templates/back_end/registrar.html",context)  
    
    
    
    