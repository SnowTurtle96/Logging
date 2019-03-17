import ast
import json

from twisted.internet.protocol import ClientFactory, Protocol
import logging

from Node1.DHT.initialization import Initialization


class DHTProtocol(Protocol):

    def connectionMade(self):
        data = self.factory.data
        msgCMD = "==REGISTER=="
        msg = msgCMD + str(data)
        messageToSend = bytes(msg, 'utf-8')
        self.transport.write(messageToSend)
        userInfo = logging.getLogger("1")
        print("Sending a DHT request")



    def dataReceived(self, data):
        data = data.decode('utf-8')
        print("BRILL")
        print("Incoming Data")
        print(data)
        dht = Initialization()
        data = ast.literal_eval(data)
        print(data)
        dht.loadDHTInformation()
        print("Finger table local")
        print(dht.fingerTable.toDict())
        dht.fingerTable.nodeid = data['nodeid']
        dht.fingerTable.successor = data['successor']
        dht.fingerTable.predecessor = data['predecessor']
        dht.writeDHTInformation()

        """Update your new neighbouring nodes and confirm that they have the write information"""








class DHTFactory(ClientFactory):
    protocol = DHTProtocol

    def __init__(self, data):
        self.data = data
