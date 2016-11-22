class Query(object):
    statements  = None
    order       = None
    binds       = None
    query       = None
    select      = None
    table       = None
    
    def __init__(self,Model):
        from Lib.DAO.Dao import Dao
        self.statements = []
        self.binds      = []
        self.order      = []
        self.query      = ''
        self.table      = Dao.getTable(Model)
        
    def add(self,Statement):
        if Statement.__class__.__name__ == 'Order':
            self.order.append(Statement)
        else:
            self.statements.append(Statement)
    
    def prepare(self):
        if self.statements:
            for pos, S in enumerate(self.statements):
                S.prepare(self, pos)
        if self.order:
            for pos, O in enumerate(self.order):
                O.prepare(self,pos)
        self.select = "SELECT * FROM {}".format(self.table)        
    