import pymssql
from pymssql import output
from pymssql import _mssql

import json

class WrapperDB:
    
    conn = 0
    
    #def __init__(self, server="PCPAOLO\SQLEXPRESS", user="sa", password="Password1!", database="5DINF", port="1433"):
    #def __init__(self, server="192.168.40.16\\SQLEXPRESS", user="CRD2122",
    def __init__(self, server="5.172.64.20\\SQLEXPRESS", user="CRD2122",
               password="xxx123##", database="CRD2122"):
        self._server=server
        self._user=user
        self._password=password
        self._database=database
        
        
    def connetti(self):
        #connessione
        try:
            WrapperDB.conn = pymssql.connect(server = self._server, user = self._user, \
                        password = self._password, database = self._database)
            #print(f"\nConnessione effettuata! (DB: {self._database})\n")
            return WrapperDB.conn	
        except _mssql.MssqlDriverException:
            print("A MSSQLDriverException has been caught.")
        except _mssql.MssqlDatabaseException as e:
            print("A MSSQLDatabaseException has been caught.")
            print('Number = ',e.number)
            print('Severity = ',e.severity)
            print('State = ',e.state)
            print('Message = ',e.message)  
        except Exception as err: 
            print("********** ERRORE [connetti] **********")
            print(str(err))     
            print("***************************************")     
        return 


    def disconnetti(self, co):
        #disconnessione	
        try:
            co.close()
        #    print(f"\nCHIUSURA connessione! (DB: {self._database})\n") 
        #except:
        #    print(f"\nCHIUSURA connessione NON riuscita! (DB: {self._database})\n")
        #    return 0
        except Exception as err: 
            print("********** ERRORE [disconnetti] **********")
            print(str(err))     
            print("******************************************")     
        
    
    
    def getEsemplari(self, as_dict = False, id=-1):
        id = int(id)
        conn = self.connetti()
        lista = []
        try:
            cur = conn.cursor(as_dict = as_dict)
            query = "SELECT * FROM V_Esemplari" + (" WHERE id = %d" if id != -1 else "")
            cur.execute(query, (id) if id != -1 else ())
            lista = cur.fetchall()
        except Exception as err: 
            print(f"********** ERRORE [select V_Esemplari] **********")
            print(str(err))     
            print("*******************************************")
        self.disconnetti(conn)
        return lista[0] if len(lista) == 1 else lista
  
  
    def getLog(self, as_dict = False, id=-1):
        id = int(id)
        conn = self.connetti()
        lista = []
        try:
            cur = conn.cursor(as_dict = as_dict)
            query = "SELECT * FROM V_Log" + (" WHERE id = %d" if id != -1 else "")
            cur.execute(query, (id) if id != -1 else ())
            lista = cur.fetchall()
            for x in lista:
                x['DataOra'] = str(x['DataOra'])
        except Exception as err: 
            print(f"********** ERRORE [select V_Log] **********")
            print(str(err))     
            print("*******************************************")   
        self.disconnetti(conn)
        return lista[0] if len(lista) == 1 else lista
        
    def addLog(self, parametri):
        conn = self.connetti() 
        try:
            cursore = conn.cursor()
            sql = "INSERT INTO V_Log (DataOra, Motivo, IDEsemplari) VALUES (%s , %s, %d); SELECT max(id) FROM V_Log"
            cursore.execute(sql, parametri)
            id = cursore.fetchall()[0][0]
            conn.commit()
        except Exception as err: 
            print("********** ERRORE [insert V_Log] **********")
            print(str(err))     
            print("*********************************************")  
            id = -1
        self.disconnetti(conn)
        return {"id": id} if id != -1 else -1
    
    def modifyLog(self, id, parametri):
        ret = True
        conn = self.connetti() 
        try:
            parametri = parametri + (id,)
            cursore = conn.cursor()
            sql = "UPDATE V_Log SET DataOra = %s, Motivo = %s, IDEsemplari = %d WHERE ID = %d"
            cursore.execute(sql, parametri)
            conn.commit()

            if (cursore.rowcount < 1):
                ret = False
        except Exception as err:
            print("********** ERRORE [update V_Log] **********")
            print(str(err))     
            print("********************************************")  
            ret = False
        self.disconnetti(conn)
        return {"id": id} if ret else -1
    
    
    def deleteLog(self, id):
        ret = True
        conn = self.connetti() 
        try:
            cursore = conn.cursor()
            sql = "DELETE V_Log WHERE id = %d"
            cursore.execute(sql, id)
            conn.commit()   

            if (cursore.rowcount < 1):
                ret = False        
        except Exception as err:
            print("********** ERRORE [delete V_Log] **********")
            print(str(err))     
            print("*******************************************")              
            ret = False
        self.disconnetti(conn)
        return {"id": id} if ret else -1
    
    
    
    
    
    def getSpecie(self, as_dict = False, nome=-1):
        conn = self.connetti()
        lista = []
        try:
            cur = conn.cursor(as_dict = as_dict)
            query = "SELECT * FROM V_Specie" + (" WHERE Nome = %s" if nome != -1 else "")
            cur.execute(query, (nome) if nome != -1 else ())
            lista = cur.fetchall()
        except Exception as err: 
            print(f"********** ERRORE [select V_Specie] **********")
            print(str(err))     
            print("*******************************************")   
        self.disconnetti(conn)
        return lista[0] if len(lista) == 1 else lista
        
    def addSpecie(self, parametri):
        conn = self.connetti() 
        nome = 1
        try:
            cursore = conn.cursor()
            sql = "INSERT INTO V_Specie (Nome, Tipo) VALUES (%s , %s)"
            cursore.execute(sql, parametri)
            conn.commit()
        except Exception as err: 
            print("********** ERRORE [insert V_Specie] **********")
            print(str(err))     
            print("*********************************************")  
            nome = -1
        self.disconnetti(conn)
        return {"Nome": parametri[0]} if nome != -1 else -1
    
    def modifySpecie(self, nome, parametri):
        ret = True
        conn = self.connetti() 
        try:
            parametri = parametri + (nome,)
            cursore = conn.cursor()
            sql = "UPDATE V_Specie SET Nome = %s, Tipo = %s WHERE Nome = %d"
            cursore.execute(sql, parametri)
            conn.commit()

            if (cursore.rowcount < 1):
                ret = False
        except Exception as err:
            print("********** ERRORE [update V_Specie] **********")
            print(str(err))     
            print("********************************************")  
            ret = False
        self.disconnetti(conn)
        return {"nome": nome} if ret else -1
    
    
    def deleteSpecie(self, nome):
        ret = True
        conn = self.connetti() 
        try:
            cursore = conn.cursor()
            sql = "DELETE V_Specie WHERE Nome = %d"
            cursore.execute(sql, nome)
            conn.commit()   

            if (cursore.rowcount < 1):
                ret = False        
        except Exception as err:
            print("********** ERRORE [delete V_Specie] **********")
            print(str(err))     
            print("*******************************************")              
            ret = False
        self.disconnetti(conn)
        return {"nome": nome} if ret else -1
    
    
    
    
  
  
    def getCibo(self, as_dict = False, id=-1):
        id = int(id)
        conn = self.connetti()
        lista = []
        try:
            cur = conn.cursor(as_dict = as_dict)
            query = "SELECT * FROM V_Cibo" + (" WHERE ID = %d" if id != -1 else "")
            cur.execute(query, (id) if id != -1 else ())
            lista = cur.fetchall()
            for x in lista:
                x['PianoTemporale'] = str(x['PianoTemporale'])
        except Exception as err: 
            print(f"********** ERRORE [select V_Cibo] **********")
            print(str(err))     
            print("*******************************************")   
        self.disconnetti(conn)
        return lista[0] if len(lista) == 1 else lista
        
    def addCibo(self, parametri):
        conn = self.connetti() 
        try:
            cursore = conn.cursor()
            sql = "INSERT INTO V_Cibo (IDEsemplari, Tipo, PianoTemporale) VALUES (%d , %s, %s); SELECT max(id) FROM V_Cibo"
            cursore.execute(sql, parametri)
            id = cursore.fetchall()[0][0]
            conn.commit()
        except Exception as err: 
            print("********** ERRORE [insert V_Cibo] **********")
            print(str(err))     
            print("*********************************************")  
            id = -1
        self.disconnetti(conn)
        return {"id": id} if id != -1 else -1
    
    def modifyCibo(self, id, parametri):
        ret = True
        conn = self.connetti() 
        try:
            parametri = parametri + (id,)
            cursore = conn.cursor()
            sql = "UPDATE V_Cibo SET IDEsemplari = %d, Tipo = %s, PianoTemporale = %s WHERE ID = %d"
            cursore.execute(sql, parametri)
            conn.commit()

            if (cursore.rowcount < 1):
                ret = False
        except Exception as err:
            print("********** ERRORE [update V_Cibo] **********")
            print(str(err))     
            print("********************************************")  
            ret = False
        self.disconnetti(conn)
        return {"id": id} if ret else -1
    
    
    def deleteCibo(self, id):
        ret = True
        conn = self.connetti() 
        try:
            cursore = conn.cursor()
            sql = "DELETE V_Cibo WHERE id = %d"
            cursore.execute(sql, id)
            conn.commit()   

            if (cursore.rowcount < 1):
                ret = False        
        except Exception as err:
            print("********** ERRORE [delete V_Cibo] **********")
            print(str(err))     
            print("*******************************************")              
            ret = False
        self.disconnetti(conn)
        return {"id": id} if ret else -1
    