import ast
import json

from twisted.internet.protocol import ClientFactory, Protocol
import logging

from Node1.DHT.initialization import Initialization


class DHTUpdateProtocol(Protocol):

    def connectionMade(self):
        data = self.factory.data
        msgCMD = "==DHTUPDATE=="
        msg = msgCMD + str(data)
        messageToSend = bytes(msg, 'utf-8')
        self.transport.write(messageToSend)
        userInfo = logging.getLogger("1")
        print("Sending DHT update")


    def dataReceived(self, data):
       print("DHT has been updated")








class DHTUpdate(ClientFactory):
    protocol = DHTUpdateProtocol

    def __init__(self, data):
        self.data = data
