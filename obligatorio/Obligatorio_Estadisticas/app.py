
from Lib.DAO.Strategy.Query import Query
from Lib.DAO.Strategy.Statements import And
from Lib.DAO.Strategy.Statements import Or
from Lib.DAO.Strategy.Statements import Like
from Lib.DAO.Strategy.Statements import Order

from App.Models.Categoria import back_end_categoria
from App.Models.Lugar import back_end_lugar
from App.Models.Evento import back_end_evento
from App.Models.Entrada import back_end_entrada
from App.Models.Asiento import back_end_asiento
from App.Models.PrecioEntrada import back_end_precioentrada


from string import upper
from datetime import datetime

'''
#Crear archivo de configuracion de conexion a la BD -> general
import shelve
d = shelve.open("config.shl")
d['general'] = {'dbhost':'localhost','dbuser':'root','dbpasswd':'','db':'obligatorio'}
d.close()
'''

def getEntidad(E, id):
    Q = Query(E)
    Q.add(And(field = "id", value = id))
    if E.loadQuery(Q):
        return E
    return None
 
'''
def getLugar(id):
    L = back_end_lugar()        
    Q = Query(L)
    Q.add(And(field = "id", value = id))
    if L.loadQuery(Q):
        return L
    return None

def getCategoria(id):
    C = back_end_categoria()
    Q = Query(C)
    Q.add(And(field = "id", value = id))
    if C.loadQuery(Q):
        return C
    return None
'''


def entradasVendidas(idEvento):
    E = back_end_entrada()    
    Q = Query(E)
    Q.add(And(field = "Evento_id", value = idEvento))
    res = E.fetchAll(Q)
    cant = len(res)    
    return str(cant)


def reporteEntradasVendidas():

    # Formato Entradas Vendidas
    formato   = {'nombre':30, 'codigo':8, 'categoria':20, 'lugar':25, 'fecha':20, 'vendidas':17}
    separador = '-------------------------------------------------------------------------------------------------------------------------'
    
    listado = 'REPORTE ENTRADAS VENDIDAS POR EVENTO\n\n'
    
    linea = '{}{}{}{}{}{}\n'.format('Nombre'.ljust(formato['nombre']), 'Codigo'.ljust(formato['codigo']), 'Categoria'.ljust(formato['categoria']), 'Lugar'.ljust(formato['lugar']), 'Fecha-Hora'.ljust(formato['fecha']), 'Entradas Vendidas'.rjust(formato['vendidas'])) 
    listado += linea

    linea = separador + '\n' 
    listado += linea

    E = back_end_evento()    
    Q = Query(E)
    Q.add(Order(field = "nombre"))
    
    for e in E.fetchAll(Q):

        # Categoria
        #C = getCategoria(e['Categoria_id'])
        C = getEntidad(back_end_categoria(), e['Categoria_id'])
        categoriaNombre = ''
        if C and C.nombre:
            categoriaNombre = C.nombre
        
        # Lugar            
        #L = getLugar(e['Lugar_id'])
        L = getEntidad(back_end_lugar(), e['Lugar_id'])
        lugarNombre = ''
        if L and L.nombre:
            lugarNombre = L.nombre
                        
        linea = '{}{}{}{}{}{}\n'.format(e['nombre'].ljust(formato['nombre']), e['codigo'].ljust(formato['codigo']), categoriaNombre.ljust(formato['categoria']), lugarNombre.ljust(formato['lugar']), str(e['fecha']).ljust(formato['fecha']), entradasVendidas(e['id']).rjust(formato['vendidas']))
        listado += linea
         
    return listado


def getPrecioAsiento(idEvento, idSector):
    PE = back_end_precioentrada()    
    Q = Query(PE)
    Q.add(And(field = "Evento_id", value = idEvento))
    Q.add(And(field = "Sector_id", value = idSector))
    
    if PE.loadQuery(Q):
        return PE.precio
    else:
        return 0


def totalFacturado(idEvento):
    E = back_end_entrada()    
    Q = Query(E)
    Q.add(And(field = "Evento_id", value = idEvento))
    importe = 0
    #Recorro las entradas vendidas del evento
    for e in E.fetchAll(Q):
        # Asiento
        A = getEntidad(back_end_asiento(), e['Asiento_id'])
        # PrecioEntrada
        precio = getPrecioAsiento(idEvento, A.Sector_id) 
        importe += precio
          
    return str(importe)


def reporteTotalFacturado():

    # Formato
    formato   = {'nombre':30, 'codigo':8, 'categoria':20, 'lugar':25, 'fecha':20, 'facturado':17}
    separador = '-------------------------------------------------------------------------------------------------------------------------'
    
    listado = 'REPORTE TOTAL FACTURADO POR EVENTO\n\n'
    
    linea = '{}{}{}{}{}{}\n'.format('Nombre'.ljust(formato['nombre']), 'Codigo'.ljust(formato['codigo']), 'Categoria'.ljust(formato['categoria']), 'Lugar'.ljust(formato['lugar']), 'Fecha-Hora'.ljust(formato['fecha']), 'Total Facturado'.rjust(formato['facturado'])) 
    listado += linea

    linea = separador + '\n' 
    listado += linea

    E = back_end_evento()    
    Q = Query(E)
    Q.add(Order(field = "nombre"))
    
    for e in E.fetchAll(Q):

        # Categoria
        C = getEntidad(back_end_categoria(), e['Categoria_id'])
        categoriaNombre = ''
        if C and C.nombre:
            categoriaNombre = C.nombre
        
        # Lugar            
        L = getEntidad(back_end_lugar(), e['Lugar_id'])
        lugarNombre = ''
        if L and L.nombre:
            lugarNombre = L.nombre
                        
        linea = '{}{}{}{}{}{}\n'.format(e['nombre'].ljust(formato['nombre']), e['codigo'].ljust(formato['codigo']), categoriaNombre.ljust(formato['categoria']), lugarNombre.ljust(formato['lugar']), str(e['fecha']).ljust(formato['fecha']), totalFacturado(e['id']).rjust(formato['facturado']))
        listado += linea
         
    return listado



opcion = ""
while opcion != "3":
    
    print ''
    print "1-Entradas vendidas por Evento"
    print "2-Total facturado por Evento"
    print "3-Salir"
    
    opcion = raw_input("Ingrese opcion:")
    
    if opcion == "1":
        
        listado = reporteEntradasVendidas()
        print '\n'
        print listado
        print ''
        
        guardar = ""
        while guardar != "N" and guardar != "S":
            guardar = raw_input("Desea guardar el listado {N, S}:")
            guardar = upper(guardar)
            if guardar == "S":
                fchhor = datetime.today().strftime("%Y-%m-%d_%H%M%S")                
                nomArch = 'Reporte_Entradas_Vendidas_por_Evento_' + fchhor + '.txt'
                F = open(nomArch, 'w')
                F.write(listado)
                F.close()                 
        
    
    elif opcion == "2":
        
        listado = reporteTotalFacturado()
        print '\n'
        print listado
        print ''
        
        guardar = ""
        while guardar != "N" and guardar != "S":
            guardar = raw_input("Desea guardar el listado {N, S}:")
            guardar = upper(guardar)
            if guardar == "S":
                fchhor = datetime.today().strftime("%Y-%m-%d_%H%M%S")                
                nomArch = 'Reporte_Total_Facturado_por_Evento_' + fchhor + '.txt'
                F = open(nomArch, 'w')
                F.write(listado)
                F.close()                 
    
    
    elif opcion != "3":
        print 'Opcion no valida'
    
print "fin..."
    