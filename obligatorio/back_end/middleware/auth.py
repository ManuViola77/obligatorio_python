from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect

class AuthUser(object):
    
    def __init__(self,get_response):
        
        # se ejeccuta una sola vez cuando se invoca al middleware AuthUser
        self.get_response = get_response
        
    def __call__(self,request):

        #verifico
        import re #expresiones regulares
        from django.contrib import messages
        if request.path_info.startswith("/back_end"):
            m = re.search("/back_end/(signin|signout|registrar)/?",request.path_info)
            if m:
                pass
            else:
                if not request.user.is_authenticated():
                    messages.error(request,"Acceso denegado")
                    return redirect("/back_end/signin/")
        
        response = self.get_response(request)
        #se ejecuta despues de llamar a middleware siguiente
        return response
