import cherrypy
import json
from Wrapper import WrapperDB



wrp = WrapperDB()

class EsemplariController(object):
    wrp = WrapperDB()
    @cherrypy.expose
    @cherrypy.tools.json_out() #NOTA: ricordarsi di aggiungere questo decoratore se vogliamo l'output in formato json!!!
    def GET(self, id=-1):
        out = self.wrp.getEsemplari(as_dict=True, id=id)
        if len(out) == 0:
            cherrypy.response.status = 404
            return {"response": "Errore 404"} 
        return out 

class SpecieController(object):
    wrp = WrapperDB()
    @cherrypy.expose
    @cherrypy.tools.json_out() 
    def GET(self, nome=-1):
        out = self.wrp.getSpecie(as_dict=True, nome=nome)
        if len(out) == 0:
            cherrypy.response.status = 404
            return {"response": "Errore 404"} 
        return out
             
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        data = cherrypy.request.json
        out = self.wrp.addSpecie((data["Nome"], data["Tipo"]))
        if (out != -1):
            return out
        else: 
            cherrypy.response.status = 500
            return {"response": "Errore 500"} 
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self, nome=-1):
        data = cherrypy.request.json
        out = self.wrp.modifySpecie(nome, (data["Nome"], data["Tipo"]))
        if (out != -1):
            return out
        else:
            cherrypy.response.status = 404
            return {"response": "Errore 404"}    
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def DELETE(self, nome=-1):
        out = self.wrp.deleteSpecie(nome)
        if (out != -1):
            return out
        else:
            cherrypy.response.status = 404
            return {"response": "Errore 404"}   

class CiboController(object):
    wrp = WrapperDB()
    @cherrypy.expose
    @cherrypy.tools.json_out() 
    def GET(self, id=-1):
        out = self.wrp.getCibo(as_dict=True, id=id)
        if len(out) == 0:
            cherrypy.response.status = 404
            return {"response": "Errore 404"} 
        return out
             
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        data = cherrypy.request.json
        out = self.wrp.addCibo((data["IDEsemplari"], data["Tipo"], data["PianoTemporale"]))
        if (out != -1):
            return out
        else: 
            cherrypy.response.status = 404
            return {"response": "Errore 404"} 
            
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self, id=-1):
        data = cherrypy.request.json
        out = self.wrp.modifyCibo(id, (data["IDEsemplari"], data["Tipo"], data["PianoTemporale"]))
        if (out != -1):
            return out
        else:
            cherrypy.response.status = 404
            return {"response": "Errore 404"}   
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def DELETE(self, id=-1):
        out = self.wrp.deleteCibo(id)
        if (out != -1):
            return out
        else:
            cherrypy.response.status = 404
            return {"response": "Errore 404"}  

class LogController(object):
    wrp = WrapperDB()
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, id=-1):
        out = self.wrp.getLog(as_dict=True, id=id)
        if len(out) == 0:
            cherrypy.response.status = 404
            return {"response": "Errore 404"} 
        return out 


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        log = cherrypy.request.json
        res = self.wrp.addLog((log["DataOra"], log["Motivo"], log["IDEsemplari"]))
        if (res != -1):
            return res 
        else: 
            cherrypy.response.status = 500
            return {"response": "Errore 500"} 


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self, id=-1):
        log = cherrypy.request.json
        res = self.wrp.modifyLog(id, (log["DataOra"], log["Motivo"], log["IDEsemplari"]))
        if (res != -1):
            return res
        else:
            cherrypy.response.status = 404
            return {"response": "Errore 404"} 
            

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def DELETE(self, id=-1):
        res = self.wrp.deleteLog(id)
        if (res != -1):
            return res
        else:
            cherrypy.response.status = 404
            return {"response": "Errore 404"} 



if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json'),('Access-Control-Allow-Origin', '*')]
        }
    }  
    
    cherrypy.tree.mount(
        root=LogController(),
        script_name='/log',
        config=conf
    )
    cherrypy.tree.mount(
        root=EsemplariController(),
        script_name='/esemplari',
        config=conf
    )
    cherrypy.tree.mount(
        root=CiboController(),
        script_name='/cibo',
        config=conf
    )
    cherrypy.tree.mount(
        root=SpecieController(),
        script_name='/specie',
        config=conf
    )
    
    cherrypy.engine.start()
    cherrypy.engine.block()