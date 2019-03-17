
from twisted.internet.protocol import ClientFactory, Protocol
import logging


class MessageProtocol(Protocol):

    def connectionMade(self):
        data = self.factory.data
        self.transport.write(data)
        userInfo = logging.getLogger("1")


    def dataReceived(self, data):
        data = data.decode('utf-8')
        f = open("nodesRecieved.json", "w+")
        f.write(str(data))
        userInfo = logging.getLogger("1")
        print("Wrong one fuck me?")




class MessageFactory(ClientFactory):
    protocol = MessageProtocol

    def __init__(self, data):
        self.data = data
