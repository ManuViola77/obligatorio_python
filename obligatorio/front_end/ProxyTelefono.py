
import decimal
import urllib2,json
from random import randint

class ProxyTelefono(object):
        
    def compra(self, numTel = None, importe = None):

        if numTel is None:
            raise Exception("Telefono no valido")
        
        if importe is None or importe <= 0:
            raise Exception("Importe no valido")
        
        try:
            #GET Telefono para saldo actual                
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            #no especifico metodo, por defecto es GET
            url = "http://localhost/portal/telefono/api/{}".format(numTel)
            datos_tel = urllib2.urlopen(url).read()
            if datos_tel:
                #convierto respuesta a diccionario
                datos_tel = json.loads(datos_tel)                     

            saldoActual = datos_tel.get("saldo")
            saldoActual = decimal.Decimal(saldoActual)
            
            if saldoActual < importe:
                raise Exception("No tiene saldo suficiente")
            
            saldo = saldoActual - importe

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
                        
            # retorno documento
            documento = str(randint(0000,99999999999))
            return documento 

                                            
        except urllib2.HTTPError as e:
            #por ejemplo server me retorno HTTP Code 404
            if e.code == 404:
                raise Exception("No se encontro el recurso")
            else:
                raise Exception(e.read(),e.code)


    def recarga(self, numTel = None, importe = None):
        
        if numTel is None:
            raise Exception("Telefono no valido")
        
        if importe is None or importe <= 0:
            raise Exception("Importe no valido")
        
        #PUT, GET a telefono            
        try:
            #GET para saldo actual
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            #no especifico metodo, por defecto es GET
            url = "http://localhost/portal/telefono/api/{}".format(numTel)                
            datos_tel = urllib2.urlopen(url).read()                
            if datos_tel: 
                #convierto respuesta a diccionario
                datos_tel = json.loads(datos_tel)
            
            saldoActual = datos_tel.get("saldo")
            saldoActual = decimal.Decimal(saldoActual)            
            saldo = saldoActual + importe

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
            return "Saldo se ha actualizado correctamente, anterior {}, actual {}".format(datos_tel.get("saldo"),datos_put.get("saldo"))
            
        except urllib2.HTTPError as e:
            #por ejemplo server me retorno HTTP Code 404
            if e.code == 404:
                raise Exception("No se encontro el recurso")
            else:
                raise Exception(e.read(),e.code)
    

