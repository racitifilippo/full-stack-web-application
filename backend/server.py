import cherrypy
#import cherrypy_cors
import json
from Wrapper import WrapperDB
#from record import record

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
    def GET(self, idEsemplari=-1):
        log = self.wrp.getLog(as_dict=True)

        if (int(idEsemplari) == -1):
            return log
        else:
            log = [d for d in log if d["IDEsemplari"] == int(idEsemplari)]
            if (len(log) >= 1):
                return (log)
            else:
                cherrypy.response.status = 404
                return {} 


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        log = cherrypy.request.json
        res = self.wrp.addLog((log["dataora"], log["motivo"], log["idesemplari"]))
        if (res != -1):
            #return { "Id": res }
            return { "id": res }
        else: 
            cherrypy.response.status = 500
            return {}


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    #@cherrypy.tools.accept(media='text/plain')
    def PUT(self, id=-1):
        log = cherrypy.request.json
        res = self.wrp.modifyLog (log["dataora"], log["motivo"], log["idesemplari"])
        if (bool(res)):
            return id
        else:
            cherrypy.response.status = 404
            return { "Id": id } 
            

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def DELETE(self, id=-1):
        res = self.wrp.deleteLog(id)
        if (res == True):
            return {}
        else:
            cherrypy.response.status = 404
            return {}



if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Access-Control-Allow-Origin', '*')]
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