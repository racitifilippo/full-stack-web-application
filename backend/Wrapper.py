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
        
    
    
    def getEsemplari(self, as_dict = False):
        conn = self.connetti()
        lista = []
        try:
            cur = conn.cursor(as_dict = as_dict)
            query = "SELECT * FROM V_Esemplari"
            cur.execute(query)
            lista = cur.fetchall()
        except Exception as err: 
            print(f"********** ERRORE [select V_Esemplari] **********")
            print(str(err))     
            print("*******************************************")   
        self.disconnetti(conn)
        return lista
  
  
    def getLog(self, as_dict = False):
        conn = self.connetti()
        lista = []
        try:
            cur = conn.cursor(as_dict = as_dict)
            query = "SELECT * FROM V_Log"
            cur.execute(query)
            lista = cur.fetchall()
        except Exception as err: 
            print(f"********** ERRORE [select V_Log] **********")
            print(str(err))     
            print("*******************************************")   
        self.disconnetti(conn)
        
        for x in lista:
            x['DataOra'] = str(x['DataOra'])
        return lista
        
    def addLog(self, parametri):
        conn = self.connetti() 
        ret = True
        try:
            cursore = conn.cursor()
            sql = "INSERT INTO V_Log (dataora, motivo, idesemplari) VALUES (%s , %s, %d)"
            cursore.execute(sql, parametri)
            conn.commit()
        except Exception as err: 
            print("********** ERRORE [insert V_Log] **********")
            print(str(err))     
            print("*********************************************")  
            ret = False
        self.disconnetti(conn)
        return ret
    
    def modifyLog(self, id, parametri):
        ret = True
        conn = self.connetti() 
        try:
            parametri = parametri + (id,)
            cursore = conn.cursor()
            sql = "UPDATE V_Log SET dataora = %s, motivo = %s, idesemplari = %d WHERE ID = %d"
            cursore.execute(sql, parametri)
            conn.commit()
            #se l'id passato non esiste restituisco comunque False
            if (cursore.rowcount < 1):
                ret = False
        except Exception as err:
            print("********** ERRORE [update V_Log] **********")
            print(str(err))     
            print("********************************************")  
            ret = False
        self.disconnetti(conn)
        return ret
    
    
    def deleteLog(self, id):
        ret = True
        conn = self.connetti() 
        try:
            cursore = conn.cursor()
            sql = "DELETE V_Log WHERE id = %d"
            cursore.execute(sql, id)
            conn.commit()   
            #se l'id passato non esiste restituisco comunque False
            if (cursore.rowcount < 1):
                ret = False        
        except Exception as err:
            print("********** ERRORE [delete V_Log] **********")
            print(str(err))     
            print("*******************************************")              
            ret = False
        self.disconnetti(conn)
        return ret
    
    
    
    
    
    def getSpecie(self, as_dict = False):
        conn = self.connetti()
        lista = []
        try:
            cur = conn.cursor(as_dict = as_dict)
            query = "SELECT * FROM V_Specie"
            cur.execute(query)
            lista = cur.fetchall()
        except Exception as err: 
            print(f"********** ERRORE [select V_Specie] **********")
            print(str(err))     
            print("*******************************************")   
        self.disconnetti(conn)
        return lista
        
    def addSpecie(self, parametri):
        conn = self.connetti() 
        ret = True
        try:
            cursore = conn.cursor()
            sql = "INSERT INTO V_Specie (nome, tipo) VALUES (%s , %s)"
            cursore.execute(sql, parametri)
            conn.commit()
        except Exception as err: 
            print("********** ERRORE [insert V_Specie] **********")
            print(str(err))     
            print("*********************************************")  
            ret = False
        self.disconnetti(conn)
        return ret
    
    def modifySpecie(self, id, parametri):
        ret = True
        conn = self.connetti() 
        try:
            parametri = parametri + (id,)
            cursore = conn.cursor()
            sql = "UPDATE V_Specie SET nome = %s, tipo = %s WHERE ID = %d"
            cursore.execute(sql, parametri)
            conn.commit()
            #se l'id passato non esiste restituisco comunque False
            if (cursore.rowcount < 1):
                ret = False
        except Exception as err:
            print("********** ERRORE [update V_Specie] **********")
            print(str(err))     
            print("********************************************")  
            ret = False
        self.disconnetti(conn)
        return ret
    
    
    def deleteSpecie(self, id):
        ret = True
        conn = self.connetti() 
        try:
            cursore = conn.cursor()
            sql = "DELETE V_Specie WHERE id = %d"
            cursore.execute(sql, id)
            conn.commit()   
            #se l'id passato non esiste restituisco comunque False
            if (cursore.rowcount < 1):
                ret = False        
        except Exception as err:
            print("********** ERRORE [delete V_Specie] **********")
            print(str(err))     
            print("*******************************************")              
            ret = False
        self.disconnetti(conn)
        return ret
    
    
    
    
    def getCibo(self, as_dict = False):
        conn = self.connetti()
        lista = []
        try:
            cur = conn.cursor(as_dict = as_dict)
            query = "SELECT * FROM V_Cibo"
            cur.execute(query)
            lista = cur.fetchall()
        except Exception as err: 
            print(f"********** ERRORE [select V_Cibo] **********")
            print(str(err))     
            print("*******************************************")   
        self.disconnetti(conn)
        return lista
        
    def addCibo(self, parametri):
        conn = self.connetti() 
        ret = True
        try:
            cursore = conn.cursor()
            sql = "INSERT INTO V_Cibo (idesemplari, tipo, PianoTemporale) VALUES (%d , %s, %s)"
            cursore.execute(sql, parametri)
            conn.commit()
        except Exception as err: 
            print("********** ERRORE [insert V_Cibo] **********")
            print(str(err))     
            print("*********************************************")  
            ret = False
        self.disconnetti(conn)
        return ret
    
    def modifyCibo(self, id, parametri):
        ret = True
        conn = self.connetti() 
        try:
            parametri = parametri + (id,)
            cursore = conn.cursor()
            sql = "UPDATE V_Cibo SET idesemplari = %d, tipo = %s, pianotemporale = %s WHERE ID = %d"
            cursore.execute(sql, parametri)
            conn.commit()
            #se l'id passato non esiste restituisco comunque False
            if (cursore.rowcount < 1):
                ret = False
        except Exception as err:
            print("********** ERRORE [update V_Cibo] **********")
            print(str(err))     
            print("********************************************")  
            ret = False
        self.disconnetti(conn)
        return ret
    
    
    def deleteCibo(self, id):
        ret = True
        conn = self.connetti() 
        try:
            cursore = conn.cursor()
            sql = "DELETE V_Cibo WHERE id = %d"
            cursore.execute(sql, id)
            conn.commit()   
            #se l'id passato non esiste restituisco comunque False
            if (cursore.rowcount < 1):
                ret = False        
        except Exception as err:
            print("********** ERRORE [delete V_Cibo] **********")
            print(str(err))     
            print("*******************************************")              
            ret = False
        self.disconnetti(conn)
        return ret
        
    # anche per specie e cibo
    