import cherrypy
import json
from Wrapper import WrapperDB

wrp = WrapperDB()
#@cherrypy.expose

class EsemplariController(object):
    wrp = WrapperDB()
    @cherrypy.expose
    @cherrypy.tools.json_out() #NOTA: ricordarsi di aggiungere questo decoratore se vogliamo l'output in formato json!!!
    def GET(self, id=-1):
        log = self.wrp.getEsemplari(as_dict=True, id=id)
        if len(log) == 0:
            cherrypy.response.status = 404
            return {"response": "Errore 404"} 
        return log

class LogController(object):
    wrp = WrapperDB()
    @cherrypy.expose
    @cherrypy.tools.json_out() #NOTA: ricordarsi di aggiungere questo decoratore se vogliamo l'output in formato json!!!
    def GET(self, id=-1):
        log = self.wrp.getLog(as_dict=True, id=id)
        if len(log) == 0:
            cherrypy.response.status = 404
            return {"response": "Errore 404"} 
        return log
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        log = cherrypy.request.json
        ris = self.wrp.addLog((log["dataora"], log["motivo"], log["idesemplari"]))
        if (ris != -1):
            return ris
        else: 
            cherrypy.response.status = 404
            return {"response": "Errore 404"}


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self, id=-1):
        log = cherrypy.request.json
        res = self.wrp.modifyLog(id=id, parametri=(log["dataora"], log["motivo"], log["idesemplari"]))
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

    # cherrypy.quickstart(LogController(), '/log')
    
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
    
    cherrypy.engine.start()
    cherrypy.engine.block()