import ast
import json

from twisted.internet.protocol import ClientFactory, Protocol
import logging



class DHTSearchReturnProtocol(Protocol):

    def connectionMade(self):
        data = self.factory.data
        msgCMD = "==DHTSEARCHRETURN=="
        msg = msgCMD + str(data)
        messageToSend = bytes(msg, 'utf-8')
        self.transport.write(messageToSend)
        userInfo = logging.getLogger("1")
        print("Sending DHT user data request")


    def dataReceived(self, data):
       print("DHT has been updated")








class DHTSearchReturn(ClientFactory):
    protocol = DHTSearchReturnProtocol

    def __init__(self, data):
        self.data = data
