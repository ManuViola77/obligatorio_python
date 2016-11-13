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
    template = loader.get_template('categorias/templates/index.html')
    usuario = request.GET.get("usuario")
    buscar = request.GET.get("buscar") # buscar = nombre del campo que quiero o del parametro de url
    pagina = request.GET.get("pagina")
    message = get_messages(request)
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
        paginator = Paginator(categorias,8)
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
    render['messages'] = message
    # template tiene parametro {} diccionario de parametros que envio para el template
    return HttpResponse(template.render(render,request))

def save(request,id = None):   
    template    = loader.get_template('categorias/templates/save.html') 
    render      = {} #diccionario para pasar a la vista
    C           = Categoria() #instancio Categoria
    try:
        if id:#Update
            try:
                C = Categoria.objects.get(pk=id)
            except Categoria.DoesNotExist:
                messages.error(request,'Identificador no valido')
                return redirect('/back_end/categorias')
        #si postean form
        do_submit = request.POST.get("do_submit")
        if do_submit:
            for key,value in request.POST.items():
                if hasattr(C, key):
                    setattr(C, key, value)            
            
            required = ['codigo','nombre']
            for r in required:
                if not getattr(C, r):
                    raise Exception("Se deben ingresar los campos Codigo y Nombre.")
            
            #valido por ej que no exista codigo
            try:
                C2 = Categoria.objects.get(codigo=C.codigo)
                if id:
                    if C2 != C:
                        raise Exception("Codigo de Categoria {} ya existe ({})".format(C.codigo,C2.nombre))
                else:
                    raise Exception("Codigo de Categoria {} ya existe ({})".format(C.codigo,C2.nombre))
                
            except Categoria.DoesNotExist:
                pass
            C.save()
            
            if not id:
               C = None
            render['success'] = "la categoria se ha {} correctamente...".format('actualizado' if id else 'ingresado')  
            
            
    except Exception as e:
        #Si "algo" me lanza una exception, lo muestro en el template
        render['error'] = e
    #render["id"] = id
    render["C"] = C
    return HttpResponse(template.render(render,request))


def delete(request,id):
    error = False
    msg   = ''
    if not id:
        error = True
        msg   = "Identificador no valido"
    else:
        try:
            C = Categoria.objects.get(pk = id)
        except Categoria.DoesNotExist:
            error = True
            msg   = "Identificador no valido"
    if not error:       
        C.delete()
        messages.success(request,"La Categoria se ha eliminado correctamente...")
    else:
        messages.error(request,msg)
    return redirect("/back_end/categorias")

