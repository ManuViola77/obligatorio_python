from MySQLdb.connections import Connection
from Lib.DAO.DataAccessResult import DataAccessResult

class DataAccess(Connection,object):
    __instance = None
    
    #Redefino constructor para obtener unica instancia
    def __new__(self, *args, **kargs):
        '''
        if not self.__instance:
            self.__instance = super(DataAccess,self).__new__(self,*args,**kargs)
        return self.__instance
        '''
        self.__instance = super(DataAccess,self).__new__(self,*args,**kargs)
        return self.__instance

    def __init__(self,host,user,passwd,db):
        super(DataAccess, self.__instance).__init__(host,user,passwd,db)
        
    #Ejecutar sentencia
    def execute(self,sql, binds):
        DAR = DataAccessResult(self)
        #print "en execute de DataAccess, sql: {}, binds: {}".format(sql,binds)
        DAR.execute(sql,binds)
        self.commit()
        return DAR.lastrowid
    
    #Retornar instancia resultado de acceso a datos
    def retrieve(self,sql, binds):
        DAR = DataAccessResult(self)
        DAR.execute(sql, binds)
        return DAR