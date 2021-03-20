from flask import jsonify

class GateManager:
    def getGate(self, userId):
        #TODO: search the DB for all gates of userId
        
        ret = [{'name':'primo', 'location':'casa', 'state':'open', 'id':'1'}, 
        {'name':'secondo', 'location':'lavoro', 'state':'closed', 'id':'2'}]
        return ret

    def addGate(self, gate):
        #TODO: add gate to the DB
        return True

    def checkGate(self, gate):
        #TODO: implement checks on the gate parameters
        return True

    def exists(self, gate):
        #TODO: check if gate already exists
        return False