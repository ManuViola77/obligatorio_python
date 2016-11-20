from Lib.DAO.DataAccess import DataAccess
from Lib.Extra.Config import Config
from datetime import datetime

class Dao(object):
    
    DA = None
    
    def __init__(self):
        try:
            Conf = Config() 
            self.DA = DataAccess(Conf.dbhost,Conf.dbuser, Conf.dbpassword, Conf.db)
        except Exception as e:
            # log de error en archivo con fecha datetime!
            raise Exception("Lo sentimos, hubo un error al conectarse al servidor...")
            
    @staticmethod
    def getTable(Model):
        return Model.__class__.__name__.lower()
    
    def fetchAll(self,Model, Q = None):
        if Q is not None:
            sql     = Q.prepare()
            sql     = Q.select+Q.query
            binds   = Q.binds
        else:
            sql     = "SELECT * FROM {}".format(self.getTable(Model))
            binds   = []
        return self.DA.retrieve(sql,binds).fetchAll()
        #armo query 
        #retorno de DA que devuelve DAR, invocando fetchAll()
    def delete(self,Model,Q = None):
        if Model.id:
            if Q is not None:
                sql     = Q.prepare()
                sql     = Q.delete+Q.query
                binds   = Q.binds
            else:
                sql     = "DELETE FROM {}".format(self.getTable(Model))
                binds   = []
            self.DA.execute(sql,binds)

    def load(self, Model, Q = None):
        if Q is not None:
            sql     = Q.prepare()
            sql     = Q.select+Q.query
            binds   = Q.binds
        else:
            sql     = "SELECT * FROM {}".format(self.getTable(Model))
            binds   = []
        row = self.DA.retrieve(sql,binds).fetch()
        if row:
            for key, value in row.items():
                setattr(Model, key, value)
            return True
        return False
            
            
            
            
            
    def update(self, Model,Q = None):
        if Model.id:
            #Model.actualizado = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            attributes = Model.toArray()
            if attributes:
                values = ''
                for key,value in attributes.items():
                    values += ",{} = '{}'".format(key,value)
                if values:
                    values = values[1:]
                    #query  = "UPDATE {} set {} WHERE id = '{}'". \
                    #format(self.getTable(Model), values, Model.id)
                    if Q is not None:
                        sql     = Q.prepare()
                        sql     = Q.select+Q.query
                        binds   = Q.binds
                    else:
                        sql     = "UPDATE {} set {} ".format(self.getTable(Model),values)
                        binds   = []
                self.DA.execute(sql,binds)
    
    
    def create(self, Model):
        #Model.creado = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        attributes = Model.toArray()
        if attributes:
            fields = ''
            values = ''
            for key, value in attributes.items():
                #no inserto id ni actualizado
                if key != 'id' and key != 'actualizado':
                    fields += ",{}".format(key)
                    values += ",'{}'".format(value)
                
            if values:
                #slicing
                values = values[1:]
                fields = fields[1:]
                query = "INSERT INTO {} ({}) VALUES ({})". \
                format(self.getTable(Model), fields, values)
                #seteo atributo id que genera base de datos
                setattr(Model, "id", self.DA.execute(query))
            
            
            
            
        
        
    
    def __del__(self):
        #me desconecto de servidor cuando se termine ejecucion de appQuery
        try:
            if self.DA.open:
                self.DA.close()
        except Exception:
            pass