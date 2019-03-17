"""Register"""
import json

from twisted.internet.protocol import ClientFactory, Protocol
import logging


class MessageCProto(Protocol):
    userInfo = logging.getLogger("1")
    def connectionMade(self):
        # data = self.factory.data.toDict(self.factory.data)
        registerCMD = "==REGISTER=="
        data = registerCMD + self.factory.data
        data = json.dumps(data)
        dataAsBytes = bytes(data, 'utf-8')
        self.userInfo.info("Sending" + data)
        self.transport.write(dataAsBytes)

    def dataReceived(self, data):
        self.userInfo.info("Registered")
        data = data.decode('utf-8')
        f = open("nodesRecieved.json", "w+")
        f.write(str(data))
        print("We should now register for a fucking DHT?")


class MessageCFactory(ClientFactory):
    protocol = MessageCProto

    def __init__(self, data):
        self.data = data
