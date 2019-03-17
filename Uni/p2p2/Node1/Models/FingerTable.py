import socket

from Node1.Models.User import User


class FingerTable():
    """Zero is a placeholder for an uninitiazlied finger table or DHT"""
    user = User()
    user = user.toDict()
    successor = user
    predecessor = user
    nodeid = user
    finger1 = user
    finger2 = user



    def toDict(self):
        return {"successor":self.successor, "predecessor":self.predecessor, "nodeid":self.nodeid}

    def addSucessor(self, user):
       updateDHT = {}
       self.successor = user.toDict
       updateDHT["successor"] = user.toDict()
       return updateDHT

    def addPredecessor(self, user):

        updateDHT = {}
        self.successor = user.toDict
        updateDHT["predecessor"] = user.toDict()
        return updateDHT

    def addFingerNode1(self, user):

        updateDHT = {}
        self.finger1 = user.toDict
        updateDHT["fingernode1"] = user.toDict()
        return updateDHT

    def addFingerNode2(self, user):

        updateDHT = {}
        self.finger2 = user.toDict
        updateDHT["fingernode2"] = user.toDict()
        return updateDHT

    def setNode(self, user):
        updateDHT = {}
        self.nodeid = user.toDict
        updateDHT["nodeid"] = user.toDict()
        return updateDHT


