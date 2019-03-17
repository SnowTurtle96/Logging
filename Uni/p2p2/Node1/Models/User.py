import hashlib
import json
import socket


class User():
    ip = ''
    port = ''
    user = ''
    publicKey = ''
    nodeid = ''

    def __str__(self):
        return (self.ip + self.port + self.user + self.publicKey + self.nodeid)

    def toDict(self):
        return {"ip":self.ip, "port":self.port, "user":self.user, "nodeid":self.nodeid, "publickey":self.publicKey}


    def generateID(self):
        """Set this variable to whatever we want to generate node ids from"""
        print("This is what we are generating nodeID from: " + self.user)

        hashed_file_value = hashlib.sha256(self.user.encode('utf-8')).hexdigest()
        return str(hashed_file_value)


