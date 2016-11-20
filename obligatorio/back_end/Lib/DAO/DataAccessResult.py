from MySQLdb.cursors import Cursor

# Nivel de abstraccion para DAO
class DataAccessResult(Cursor,object):
    
    # conjunto de resultados 
    def fetchAll(self):
        rows = super(DataAccessResult,self).fetchall()
        # description = lista de nombres de campos (= el field[0]), tipos, etc
        fields = [field[0] for field in self.description] 
        result = []
        #fetch all retorna tupla vacia si no hay datos
        if len(rows):
            for row in rows:
                data = {}
                for key,value in enumerate(row):
                    data[fields[key]] = value
                result.append(data)
        return result  
    
    # 1 resultado
    def fetch(self):
        rows = super(DataAccessResult,self).fetchone()
        fields = [field[0] for field in self.description]
        data = {}
        #fetchone retorna None si no hay resultados
        if rows is not None:
            for key,value in enumerate(rows):
                data[fields[key]] = value
        return data
