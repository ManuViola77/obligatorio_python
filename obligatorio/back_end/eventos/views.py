from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator,InvalidPage,PageNotAnInteger
from django import forms

# Create your views here.

from back_end.Categoria import Categoria
from back_end.Lugar import Lugar
from back_end.Evento import Evento
from back_end.Afiche import Afiche,AficheForm

def index(request):
    #instancio Template
    template = loader.get_template('eventos/templates/index.html')
    usuario = request.GET.get("usuario")
    buscar = request.GET.get("buscar") # buscar = nombre del campo que quiero o del parametro de url
    pagina = request.GET.get("pagina")
    message = get_messages(request)
    render = {}
    eventos = Evento.objects.all()
    
    error = False
    if not pagina:
        pagina = 1
        
    if buscar is not None:
        eventos = eventos.filter(nombre__icontains=buscar)
    try:
        #Query set y cantidad de registros por pagina
        eventos = eventos.order_by('nombre','codigo') #'-nombre' para descendente
        paginator = Paginator(eventos,8)
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
    render['messages'] = message
    # template tiene parametro {} diccionario de parametros que envio para el template
    return HttpResponse(template.render(render,request))

def save(request,id = None):   
    template    = loader.get_template('eventos/templates/save.html') 
    render      = {} #diccionario para pasar a la vista
    E           = Evento() #instancio Evento
    categorias = Categoria.objects.all()
    lugares = Lugar.objects.all()
    try:
        if id:#Update
            try:
                E = Evento.objects.get(pk=id)
            except Evento.DoesNotExist:
                messages.error(request,'Identificador no valido')
                return redirect('/back_end/eventos')
        #si postean form
        #form = forms(request.POST, request.FILES)
        #if form.is_valid():
        #E.afiche = request.FILES['afiche']  
        A = None    
        try:
            if request.POST:
                print "Entre al post para afiche"
                unForm = AficheForm(request.POST,request.FILES)
                if unForm.is_valid():
                    #sino lanzo una excepcion desde metodo clean
                    print "Afiche valido"
                    A = unForm.save()
                    print "afiche exitoso"
                    render["success"] = "Se grabo ok"
                else:
                    print "Error en afiche - puede ser que venia vacio"
                    #render["error"] = unForm.errors
        except Exception as e:
            render["error"] = e    
            
               
        do_submit = request.POST.get("do_submit")
        if do_submit:
            for key,value in request.POST.items():
                if hasattr(E, key):
                    setattr(E, key, value)            
            
            #grabo categoria
            if request.POST.get("categoria"):
                #programacion defensiva (validar que exista pk)
                CategoriaEvento = Categoria.objects.get(pk=request.POST.get("categoria"))
                E.Categoria = CategoriaEvento
                
            #grabo lugar
            if request.POST.get("lugar"):
                #programacion defensiva (validar que exista pk)
                LugarEvento = Lugar.objects.get(pk=request.POST.get("lugar"))
                E.Lugar = LugarEvento
            
            #ver que hacer con afiche...... 
            required = ['codigo','nombre','fecha','detalle']
            for r in required:
                if not getattr(E, r):
                    raise Exception("Se deben ingresar los datos obligatorios.")
            if not E.Categoria or not E.Lugar:
                raise Exception("Se deben ingresar los datos obligatorios.")
            
            #valido por ej que no exista codigo
            try:
                E2 = Evento.objects.get(codigo=E.codigo)
                if id:
                    if E2 != E:
                        raise Exception("Codigo de Evento {} ya existe ({})".format(E.codigo,E2.nombre))
                else:
                    raise Exception("Codigo de Evento {} ya existe ({})".format(E.codigo,E2.nombre))
                
            except Evento.DoesNotExist:
                pass
            if A:
                E.Afiche = A
                
            E.save()
            
            if not id:
                E = None
            render['success'] = "El evento se ha {} correctamente...".format('actualizado' if id else 'ingresado')  
            
            
            
    except Exception as e:
        #Si "algo" me lanza una exception, lo muestro en el template
        render['error'] = e
    #render["id"] = id
    render["E"] = E
    render["categorias"] = categorias
    render["lugares"] = lugares

    return HttpResponse(template.render(render,request))


def delete(request,id):
    error = False
    msg   = ''
    if not id:
        error = True
        msg   = "Identificador no valido"
    else:
        try:
            E = Evento.objects.get(pk = id)
        except Evento.DoesNotExist:
            error = True
            msg   = "Identificador no valido"
    if not error:       
        E.delete()
        messages.success(request,"El Evento se ha eliminado correctamente...")
    else:
        messages.error(request,msg)
    return redirect("/back_end/eventos")

def display(request,id):
    template    = loader.get_template('eventos/templates/display.html') 
    render      = {} #diccionario para pasar a la vista
    if not id:
        messages.error(request,'Identificador no valido')
        return redirect('/back_end/eventos')
    else:
        try:
            E = Evento.objects.get(pk=id)
            if E.Afiche: 
                try:
                    A = Afiche.objects.get(pk = E.Afiche.id)     
                    render["A"] = A
                except Afiche.DoesNotExist:
                    raise Exception ("Afiche no existe")
        except Evento.DoesNotExist:
            messages.error(request,'Identificador no valido')
            return redirect('/back_end/eventos')
        render["E"] = E
        
        return HttpResponse(template.render(render,request))