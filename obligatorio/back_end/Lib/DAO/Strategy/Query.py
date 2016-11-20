class Query(object):
    statements  = None
    binds       = None
    query       = None
    select      = None
    delete      = None
    table       = None
    
    def __init__(self,Model):
        from Lib.DAO.Dao import Dao
        self.statements = []
        self.binds      = []
        self.query      = ''
        self.table      = Dao.getTable(Model)
        
    def add(self,Statement):
        self.statements.append(Statement)
    
    def prepare(self):
        if self.statements:
            for pos, S in enumerate(self.statements):
                S.prepare(self, pos)
        self.select = "SELECT * FROM {}".format(self.table)   
        self.delete = "DELETE FROM {}".format(self.table) 