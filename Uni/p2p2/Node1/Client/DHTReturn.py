import ast
import json

from twisted.internet.protocol import ClientFactory, Protocol
import logging



class DHTReturnProtocol(Protocol):

    def connectionMade(self):
        data = self.factory.data
        msgCMD = "==DHTRETURN=="
        msg = msgCMD + str(data)
        messageToSend = bytes(msg, 'utf-8')
        self.transport.write(messageToSend)
        userInfo = logging.getLogger("1")
        print("Sending a DHT request")


class DHTReturn(ClientFactory):
    protocol = DHTReturnProtocol

    def __init__(self, data):
        self.data = data