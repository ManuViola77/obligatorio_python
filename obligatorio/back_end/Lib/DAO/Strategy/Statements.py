import abc

class Strategy(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def prepare(self, Q, pos = 0):
        pass
    
    

class And(Strategy):
    conditions = None
    
    def __init__(self, field, value = None):
        self.conditions = {}
        if isinstance(field, dict):
            self.conditions = field
        elif field and value:
            self.conditions[field] = value
            
    def prepare(self, Q, pos = 0):
        result = ''
        if self.conditions is not None:
            for field,value in self.conditions.items():
                #Query parametrizada
                #1.Evitar SQL injection (OWASP)
                #2.Mejorar performance
                result += ' AND {} = %s'.format(field)
                Q.binds.append(value)
            result = result[4:] if pos == 0 else result
            result = " {} {}".format("" if Q.query else "WHERE",result)
            Q.query += result       
            

class Or(Strategy):
    conditions = None
    
    def __init__(self, field, value = None):
        self.conditions = {}
        if isinstance(field, dict):
            self.conditions = field
        elif field and value:
            self.conditions[field] = value
            
    def prepare(self, Q, pos = 0):
        result = ''
        if self.conditions is not None:
            for field,value in self.conditions.items():
                #Query parametrizada
                #1.Evitar SQL injection (OWASP)
                #2.Mejorar performance
                result += ' OR {} = %s'.format(field)
                Q.binds.append(value)
            result = result[3:] if pos == 0 else result
            result = " {} {}".format("" if Q.query else "WHERE",result)
            Q.query += result   
            
            
class Like(Strategy):
    conditions = None
    operand = None
    
    def __init__(self, field, value = None, exclude = True):
        self.conditions = {}
        if isinstance(field, dict):
            self.conditions = field
        elif field and value:
            self.conditions[field] = value
        self.operand = "{}".format("AND" if exclude else "OR")
           
    def prepare(self, Q, pos = 0):
        result = ''
        if self.conditions is not None:
            for field,value in self.conditions.items():
                #Query parametrizada
                #1.Evitar SQL injection (OWASP)
                #2.Mejorar performance
                result += ' {} {} like %s'.format(self.operand,field)
                Q.binds.append('%{}%'.format(value))
            result = result[len(self.operand)+1:] if pos == 0 else result
            result = " {} {}".format("" if Q.query else "WHERE",result)
            Q.query += result   
            
            
class In(Strategy):
    pass # deberes!!!!     