from Lib.DAO.Dao import Dao
class Model(object):
    DAO         = None
    id          = None
    #creado      = None
    #actualizado = None
    
    def __init__(self):
        self.DAO = Dao()
    
    def load(self):
        return self.DAO.load(self)    
    
    def delete(self):
        self.DAO.delete(self)
        
    def save(self, Q = None):
        if self.id:
            self.update(Q)
        else:
            self.create(Q)
    
    def create(self,Q = None):
        self.DAO.create(self,Q)
        
    def update(self,Q = None):
        self.DAO.update(self,Q)
        
    def fetchAll(self, Q = None):
        return self.DAO.fetchAll(self, Q)
    
    def loadQuery(self, Q = None):
        return self.DAO.loadQuery(self, Q)    
    
    def fetch(self):
        return self.DAO.fetch(self)
    
    def objects(self):
        #Model.__class__
        return self.DAO.objects(self)
    
    def toArray(self):
        attributes = {}
        for key in dir(self):
            if not callable(getattr(self, key)) and not key.startswith('__') \
            and not isinstance(getattr(self, key), Dao):
                attributes[key] = getattr(self, key)
        return attributes