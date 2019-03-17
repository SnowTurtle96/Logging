import itertools
import json
import logging
import time

from pickle import dumps, loads
from cryptography.hazmat.primitives import padding
from twisted.internet import reactor
from collections import defaultdict
from cryptography.fernet import Fernet
from Node1.Client.MessageFactory import MessageFactory
from Node1.Encryption.Encryption import Encryption
from Node1.TOR.route import Route


class OR():
    recieverIP = None
    recieverPort = None
    messageToSend = None
    routeCreated = False
    onionDict = None
    key1 = None
    key2 = None
    key3 = None
    """Before we create our onion route we need to know who we are sending our message to"""
    route = Route()

    #TODO Randomize a number below the amount of nodes in the routing table rather than always select the first 3
    #TODO Check that these nodes are alive before attempting to route through them. If not choose another node and do not add it to the onion route

    def constructRoute(self, peerList):

        currentUser = open("Models.json", "r")
        currentUser = currentUser.read()
        currentUser = json.loads(currentUser)

        self.route.hop1 = peerList['successor']
        self.route.hop2 = peerList['predecessor']

    def createKeys(self):
        key1 = Fernet.generate_key()
        key2 = Fernet.generate_key()
        key3 = Fernet.generate_key()

        self.key1 = key1
        self.key2 = key2
        self.key3 = key3

        self.exchangeKeys()

    def exchangeKeys(self):
        userInfo = logging.getLogger("1")
        userInfo.info("Exchanging Keys")
        self.loadInRecipitent()

        keyExchangeHop1 = {}
        keyExchangeHop1['CMD'] = "==CREATE=="
        keyExchangeHop1['KEY'] = self.key1
        keyExchangeHop1['NEXTHOPIP'] = self.route.hop1['ip']
        keyExchangeHop1['NEXTHOPPORT'] = self.route.hop1['port']

        keyExchangeHop2 = {}
        keyExchangeHop2['CMD'] = "==CREATE=="
        keyExchangeHop2['KEY'] = self.key2
        keyExchangeHop2['NEXTHOPIP'] = self.route.hop2['ip']
        keyExchangeHop2['NEXTHOPPORT'] = self.route.hop2['port']

        print("Key Exchange Hop 1")
        print(keyExchangeHop1)
        print("Key Exchange Hop 2")
        print(keyExchangeHop2)
        keyExchangeHop3 = {}
        keyExchangeHop3['CMD'] = "==CREATERECIPITENT=="
        keyExchangeHop3['KEY'] = self.key3
        print("Key Exchange for reciever" + str(keyExchangeHop3))

        keyExchangePackage1 = bytes(str(keyExchangeHop1), 'utf-8')
        keyExchangePackage2 = bytes(str(keyExchangeHop2), 'utf-8')
        keyExchangePackage3 = bytes(str(keyExchangeHop3), 'utf-8')

        userInfo.info("First Exchange" + str(self.route.hop1["port"]))
        reactor.connectTCP(self.route.hop1["ip"], int(self.route.hop1["port"]), MessageFactory(keyExchangePackage1))
        userInfo.info("Second Exchange" + str(self.route.hop2["port"]))
        reactor.connectTCP(self.route.hop2["ip"], int(self.route.hop2["port"]), MessageFactory(keyExchangePackage2))
        print("IP AND PORT")
        print(self.recieverIP, self.recieverPort)
        reactor.connectTCP(self.recieverIP, int(self.recieverPort), MessageFactory(keyExchangePackage3))
        self.routeCreated = True


    def encryptMsgForOnionRouting(self, msg):

        # Encrpytion is preformed First In Last Out
        # Reciever will be encrypted first working way back from OR3 TO OR1
        encryption = Encryption()

        global onionRoute
        self.loadInRecipitent()
        d3 = {"cmd": "MSG",  "msg": msg}
        print(d3)
        print("Recipitent port or IP")
        print(self.recieverIP)
        print(self.recieverPort)
        key3 = Fernet(self.key3)
        token3 = key3.encrypt(dumps(d3))
        d2 = {"cmd": "FWD", "ip": self.recieverIP, "port": self.recieverPort, "msg": token3}
        key2 = Fernet(self.key2)
        token2 = key2.encrypt(dumps(d2))
        d1 = {"cmd": "FWD", "ip": self.route.hop2['ip'], "port": self.route.hop2['port'], "msg": token2}
        key1 = Fernet(self.key1)
        token1 = key1.encrypt(dumps(d1))

        self.onionDict = token1

    def loadInRecipitent(self):
        print("Recipitent read in")
        reciever = open("messagingPartner.json", "r")
        reciever = reciever.read()
        reciever = json.loads(reciever)
        self.recieverIP = reciever['ip']
        self.recieverPort = reciever['port']
        print("Reciever")
        print(self.recieverIP)
        print(self.recieverPort)


    #Getters and Setters
    def setRecieverIP(self, recieverIP):
        self.recieverIP = recieverIP

    def setRecieverPort(self, recieverPort):
        self.recieverPort = recieverPort


