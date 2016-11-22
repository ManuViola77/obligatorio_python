from MySQLdb.cursors import Cursor

#Nivel de abstraccion para resultado de acceso a datos
class DataAccessResult(Cursor, object):
    #Conjunto de resultados
    def fetchAll(self):
        rows    = super(DataAccessResult,self).fetchall()
        fields  = [field[0] for field in self.description]
        result  = []
        #fetch all retorna tupla vacia si no hay datos
        if len(rows):
            for row in rows:
                data = {}
                for key,value in enumerate(row):
                    data[fields[key]] = value
                result.append(data)
        return result
    #1 resultado
    def fetch(self):
        rows    = super(DataAccessResult,self).fetchone()
        fields  = [field[0] for field in self.description]
        data    = {}
        #fetchone retorna None si no hay resultado
        if rows is not None:
            for key,value in enumerate(rows):
                data[fields[key]] = value
        return data