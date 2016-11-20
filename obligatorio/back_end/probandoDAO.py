from Lib.DAO.Strategy.Query import Query
from Lib.DAO.Strategy.Statements import And,Or,Like
from back_end.App.Models.Back_end_Lugar import Back_end_Lugar

try: 
    L = Back_end_Lugar()

    Q = Query(L)
    Q.add(And(field="id",value=31))
    if L.load(Q):
        print L.codigo, L.nombre
        L.delete()
    else:
        print 'id no valido'
    
    Q = Query(L)
    Q.add(And(field="id",value=30))    
    for l in L.fetchAll(Q):  # <--- esto es solo para probar
        #la query NO va como parametro en el modelo y menos desde el entorno
        print l.get("codigo"), l.get("nombre"), l.get("direccion")
        
except Exception as e:
    print e 