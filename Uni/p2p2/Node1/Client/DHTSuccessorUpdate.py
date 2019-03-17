import ast
import json

from twisted.internet.protocol import ClientFactory, Protocol
import logging



class DHTSuccessorUpdateProtocol(Protocol):

    def connectionMade(self):
        data = self.factory.data
        msgCMD = "==DHTSUCCESSOR=="
        msg = msgCMD + str(data)
        messageToSend = bytes(msg, 'utf-8')
        self.transport.write(messageToSend)
        userInfo = logging.getLogger("1")
        print("Sending DHT update")


    def dataReceived(self, data):
       print("DHT has been updated")








class DHTSuccessorUpdate(ClientFactory):
    protocol = DHTSuccessorUpdateProtocol

    def __init__(self, data):
        self.data = data
