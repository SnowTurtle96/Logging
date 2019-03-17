import ast
import datetime
import json
import logging
import time

from twisted.internet import protocol, reactor
from cryptography.fernet import Fernet
from pickle import dumps, loads

from Node1 import Models
from Node1.Client.DHTFactory import DHTFactory
from Node1.Client.DHTPredecessorUpdate import DHTPredecessorUpdate
from Node1.Client.DHTReturn import DHTReturn
from Node1.Client.DHTSearch import DHTSearch
from Node1.Client.DHTSearchReturn import DHTSearchReturn
from Node1.Client.DHTSuccessorUpdate import DHTSuccessorUpdate
from Node1.Client.RegisterFactory import MessageCFactory

from Node1.DHT.initialization import Initialization
from Node1.Client.MessageFactory import MessageFactory
from Node1.Encryption.Encryption import Encryption
from Node1.Models import User
from Node1.Models.FingerTable import FingerTable
from Node1.Utils import InitChecks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format("./", "client")),
        logging.StreamHandler()
    ])
logger = logging.getLogger(),


class ServerFactory(protocol.Protocol):
    users = []
    debuggingWindow = logging.getLogger("1")
    circuits = {}
    messageDecoderKey = {}
    dht = Initialization()
    user = User
    dhtfile = None
    initialChecks = InitChecks

    # print("\n")
    # print("\n")
    # print("CHECKS TO SEE IF FINGERTABLES ARE SAME OR SEPERATE")
    # dht1 = Initialization()
    # dht2 = Initialization()
    # dht1.fingerTable.predecessor = 1
    # dht2.fingerTable.predecessor = 2
    # print(dht1.fingerTable.toDict())
    # print(dht2.fingerTable.toDict())
    # print("\n")
    # print("\n")


    if(initialChecks.checkDHTInitialized()):
        print("Do nothing!")
    else:
        dht.loadDHTInformation()



    def dataReceived(self, data):
        logging.info("Node connecting")
        debuggingWindow = logging.getLogger("1")
        debuggingWindow.info("Incoming Data")
        data = data.decode('utf-8')
        logging.info(data)


        if "==REGISTER==" in data:
            debuggingWindow.info("Node registered")
            self.register(data)

        elif "==CREATE==" in data:
            debuggingWindow.info("Recieved a symmetric key")
            self.exchangeKeys(data)

        elif "==CREATERECIPITENT==" in data:
            debuggingWindow.info("Recieved a key for decoding messages")
            self.recieveRecipitantKey(data)

        elif "==DHTSUCCESSOR==" in data:
            debuggingWindow.info("Another node is updating our successor")
            data = data.replace('==DHTSUCCESSOR==', '')
            data = data.replace('\'', '"')
            data = json.loads(data)
            print("ISSUE" + str(data))
            self.dht.loadDHTInformation()
            self.dht.fingerTable.successor = data
            self.dht.writeDHTInformation()

        elif "==DHTPREDECESSOR==" in data:
            debuggingWindow.info("Another node is updating our predecessor")
            data = data.replace('==DHTPREDECESSOR==', '')
            data = data.replace('\'', '"')
            data = json.loads(data)
            print("ISSUE" + str(data))
            self.dht.loadDHTInformation()
            self.dht.fingerTable.predecessor = data
            self.dht.writeDHTInformation()

        elif "==DHTRETURN==" in data:
            debuggingWindow.info("DHT RETURN FROM A LONG RANGE NODE")
            data = data.replace('==DHTRETURN==', '')
            data = data.replace('\'', '"')
            data = json.loads(data)
            dht = Initialization()
            dht.loadDHTInformation()
            dht.fingerTable.nodeid = data['nodeid']
            dht.fingerTable.successor = data['successor']
            dht.fingerTable.predecessor = data['predecessor']
            dht.writeDHTInformation()


        elif "==DHTSEARCHRETURN" in data:
            debuggingWindow.info("A node has found the user from your search and has returned it to you. Messaging now enabled")
            data = data.replace("==DHTSEARCHRETURN==", '')
            data = data.replace('\'', '"')
            data = json.loads(data)

            # Write the contact information of our user to a local file for use
            file = open("messagingPartner.json", "w+")
            messagingPartnerInfo = json.dumps(data)
            file.write(messagingPartnerInfo)
            file.flush()




        elif "==DHT==" in data:
            debuggingWindow.info("Recieved a request to join the DHT")
            self.DHTPositionSearch(data)

        elif "==DHTSEARCH==" in data:
            debuggingWindow.info("REQUEST RECEIVED FOR A SEARCH OF OUR STORAGE")
            self.DHTInformationSearch(data)

        else:
            debuggingWindow.info("Onion Routing")
            self.onionRouting(data)

    def register(self, data):
        self.DHTPositionSearch(data)


    def msg(self, data):
        self.debuggingWindow.info("Receiving a message")
        data = data.replace('==MSG==', '')
        chatA = logging.getLogger("2")
        chatA.info(data)

    def combineJSONFiles(self, oldData, newUser):

        oldData = str(oldData)
        newUser = str(newUser)
        oldData = oldData.replace(']', "")
        oldData = ''.join((oldData, ','))
        newUser = ''.join((newUser, ']'))
        logging.info("Initial Data Old" + oldData)
        logging.info("Initial Data New Models" + newUser)

        sanitised = oldData + newUser
        sanitised = sanitised.replace('\'', '"')

        return sanitised

    def onionRouting(self, data):
        #Updated dict will take the current dictionary of msgs and cmds and rearrange it based on the state of the onion router and what HOP it was in the circuit
        #Fix updated dict / if statements do not update this for some weird reason
        reencoded = ast.literal_eval(data)
        print(reencoded)
        print("recipt onion")
        print(self.messageDecoderKey)
        print(self)
        try:
            print(self.circuits['key'])
            key = Fernet(self.circuits['key'])
            peeledLayer = loads(key.decrypt(reencoded))
        except:
            print("Wrong key!")
            try:
                print("recipt key")
                print(self.messageDecoderKey)
                key = Fernet(self.messageDecoderKey['key'])
                peeledLayer = loads(key.decrypt(reencoded))
            except:
                print("Wrong key2!")

        print("data")
        print(data)
        print("peeeeled")
        print(peeledLayer)
        connectingIP = self.transport.getPeer().host
        print(self.circuits)
        if(peeledLayer['cmd'] == 'FWD'):
            logging.info("Fowarding Message")
            peeledLayerToSend = bytes(str(peeledLayer['msg']), 'utf-8')
            reactor.connectTCP(peeledLayer['ip'], int(peeledLayer['port']),
                                MessageFactory(peeledLayerToSend))
            self.debuggingWindow.info(peeledLayer)
            self.debuggingWindow.info("Fowarding message to the next OR!")

        elif(peeledLayer['cmd'] == 'MSG'):
            logging.info("Recieving Message")
            self.msg(peeledLayer['msg'])

        else:
            print("Should never end up here")

    def exchangeKeys(self, data):
        data = ast.literal_eval(data)
        circuit = {
            "ip": self.transport.getPeer().host,
            "key": data['KEY'],
            "hopip": data['NEXTHOPIP'],
            "hopport": data['NEXTHOPPORT']
                     }
        self.circuits.update(circuit)
        print("data 5" + str(circuit))

    def recieveRecipitantKey(self, data):
        data = ast.literal_eval(data)
        print(data)
        messageDecoderKey = {
            "key": data['KEY']
        }
        self.messageDecoderKey.update(messageDecoderKey)

        print(self.messageDecoderKey)



    def DHTPositionSearch(self, incomingDHT):
        incomingDHT = incomingDHT.replace('==REGISTER==', '')

        incomingDHT = json.loads(incomingDHT)
        currentUser = open("Models.json", "r")
        currentUser = currentUser.read()
        currentUser = json.loads(currentUser)

        self.dht.loadDHTInformation()



        if (self.dht.fingerTable.successor['nodeid'] == '' and self.dht.fingerTable.predecessor['nodeid'] == ''):
            self.dht.fingerTable.predecessor = incomingDHT
            self.dht.fingerTable.successor = incomingDHT
            self.dht.fingerTable.nodeid = currentUser


            print("fingertable before saving" + str(self.dht.fingerTable.toDict()))

            self.dht.writeDHTInformation()
            print("This is what we are saving" + str(self.dht.fingerTable.toDict()))

            """Send back the inverse of our finger table to the new node. E.g. we are its successor and predecssor and it is ours"""
            dhtForNewNode = Initialization()
            dhtForNewNode.fingerTable.successor = currentUser
            dhtForNewNode.fingerTable.predecessor = currentUser
            dhtForNewNode.fingerTable.nodeid = incomingDHT

            reactor.connectTCP(incomingDHT['ip'], int(incomingDHT['port']), DHTReturn(dhtForNewNode.fingerTable.toDict()))
            # self.transport.write(bytes(str(dhtForNewNode.fingerTable.toDict()), 'utf-8'))

            print("fingertable reqs")
            print(str(self.dht.fingerTable.toDict()))

            """Check for edge case when we are at the start of our DHT"""
        elif(self.dht.fingerTable.nodeid['nodeid'] < self.dht.fingerTable.predecessor['nodeid']):
            print("EDGE CASE START OF DHT!")
            if(incomingDHT['nodeid'] < self.dht.fingerTable.nodeid['nodeid']):

                """This handles the remote node"""

                dhtForNewNode = Initialization()
                dhtForNewNode.fingerTable.successor = currentUser
                dhtForNewNode.fingerTable.nodeid = incomingDHT
                dhtForNewNode.fingerTable.predecessor = self.dht.fingerTable.predecessor
                print("This is what we are sending" + str(dhtForNewNode.fingerTable.toDict()))
                print("Predecessor and successor")
                print(str(self.dht.fingerTable.predecessor) + str(self.dht.fingerTable.successor))
                print("Sending incoming DHT PROBLEM" + str(incomingDHT))
                reactor.connectTCP(self.dht.fingerTable.predecessor['ip'],
                                    int(self.dht.fingerTable.predecessor['port']), DHTSuccessorUpdate(incomingDHT))

                """This handles the local node"""
                print("New predecessor: " + str(incomingDHT['nodeid']))
                self.dht.fingerTable.predecessor = incomingDHT
                self.dht.writeDHTInformation()

                reactor.connectTCP(incomingDHT['ip'], int(incomingDHT['port']), DHTReturn(dhtForNewNode.fingerTable.toDict()))
                # self.transport.write(bytes(str(dhtForNewNode.fingerTable.toDict()), 'utf-8'))


            elif(incomingDHT['nodeid'] > self.dht.fingerTable.nodeid['nodeid']):

                """This handles the remote node"""
                dhtForNewNode = Initialization()
                dhtForNewNode.fingerTable.successor = self.dht.fingerTable.successor
                dhtForNewNode.fingerTable.nodeid = incomingDHT
                dhtForNewNode.fingerTable.predecessor = currentUser
                print("This is what we are sending" + str(dhtForNewNode.fingerTable.toDict()))

                """This handles updating our old successor"""
                reactor.connectTCP(self.dht.fingerTable.successor['ip'],
                                        int(self.dht.fingerTable.successor['port']), DHTPredecessorUpdate(incomingDHT))
                print("Sending incoming DHT PROBLEM" + str(incomingDHT))



                """This handles the local node"""
                print("New successor:  " + str(incomingDHT))
                self.dht.fingerTable.successor = incomingDHT
                self.dht.writeDHTInformation()


                reactor.connectTCP(incomingDHT['ip'], int(incomingDHT['port']), DHTReturn(dhtForNewNode.fingerTable.toDict()))
                """self.transport.write(bytes(str(dhtForNewNode.fingerTable.toDict()), 'utf-8'))"""

            else:
                print("Error")

            """Check for edge case when we are at the end of our DHT"""
        elif(self.dht.fingerTable.nodeid['nodeid'] > self.dht.fingerTable.successor['nodeid']):
            print("EDGE CASE END OF DHT")
            print(self.dht.fingerTable.toDict())

            if(incomingDHT['nodeid'] > self.dht.fingerTable.nodeid['nodeid']):


                """This handles the remote node"""
                dhtForNewNode = Initialization()
                dhtForNewNode.fingerTable.successor = self.dht.fingerTable.successor
                dhtForNewNode.fingerTable.nodeid = incomingDHT
                dhtForNewNode.fingerTable.predecessor = self.dht.fingerTable.nodeid
                print("This is what we are sending" + str(dhtForNewNode.fingerTable.toDict()))

                """Update the old predecessor and inform it that we now have a new precdessor which will be its successor"""


                reactor.connectTCP(self.dht.fingerTable.predecessor['ip'],
                                int(self.dht.fingerTable.predecessor['port']), DHTSuccessorUpdate(incomingDHT))




                print("New successor: " + str(incomingDHT['nodeid']))
                print(self.dht.fingerTable.toDict())
                self.dht.fingerTable.successor = incomingDHT
                print(self.dht.fingerTable.toDict())

                self.dht.writeDHTInformation()

                reactor.connectTCP(incomingDHT['ip'],
                                   int(incomingDHT['port']), DHTReturn(dhtForNewNode.fingerTable.toDict()), 'utf-8')

                """self.transport.write(bytes(str(dhtForNewNode.fingerTable.toDict()), 'utf-8'))"""

            elif(incomingDHT['nodeid'] < self.dht.fingerTable.nodeid['nodeid']):

                """This handles the remote node"""
                dhtForNewNode = Initialization()
                dhtForNewNode.fingerTable.successor = self.dht.fingerTable.nodeid
                dhtForNewNode.fingerTable.nodeid = incomingDHT
                dhtForNewNode.fingerTable.predecessor = self.dht.fingerTable.predecessor
                print("This is what we are sending" + str(dhtForNewNode.fingerTable.toDict()))
                print("Predecessor and successor")
                print(str(self.dht.fingerTable.predecessor) + str(self.dht.fingerTable.successor))
                if (self.dht.fingerTable.predecessor['nodeid'] == self.dht.fingerTable.successor['nodeid']):
                    print("True True True bravo")
                    if (self.dht.fingerTable.predecessor != self.dht.fingerTable.nodeid):
                        reactor.connectTCP(self.dht.fingerTable.predecessor['ip'],
                                           int(self.dht.fingerTable.predecessor['port']), DHTSuccessorUpdate(incomingDHT))


                else:
                    print("False False False bollocks")

                    reactor.connectTCP(self.dht.fingerTable.successor['ip'],
                                       int(self.dht.fingerTable.successor['port']),
                                       DHTPredecessorUpdate(incomingDHT))
                    reactor.connectTCP(self.dht.fingerTable.predecessor['ip'],
                                       int(self.dht.fingerTable.predecessor['port']), DHTSuccessorUpdate(incomingDHT))

                """This handles the local node"""
                print("New predecessor: " + str(incomingDHT))
                print(self.dht.fingerTable.toDict())

                """Update the old predecessor and inform it that we now have a new precdessor which will be its successor"""

                self.dht.fingerTable.predecessor = incomingDHT
                print(self.dht.fingerTable.toDict())
                self.dht.writeDHTInformation()



                # self.transport.write(bytes(str(dhtForNewNode.fingerTable.toDict()), 'utf-8'))
                reactor.connectTCP(incomingDHT['ip'], int(incomingDHT['port']), DHTReturn(dhtForNewNode.fingerTable.toDict()))

            else:
                print("Error")
        elif(incomingDHT['nodeid'] < self.dht.fingerTable.nodeid['nodeid']):
            print("New Predecessor NO EDGE CASE")

            """This handles the remote node"""
            dhtForNewNode = Initialization()
            dhtForNewNode.fingerTable.successor = self.dht.fingerTable.nodeid
            dhtForNewNode.fingerTable.nodeid = incomingDHT
            dhtForNewNode.fingerTable.predecessor = self.dht.fingerTable.predecessor
            print("This is what we are sending" + str(dhtForNewNode.fingerTable.toDict()))

            """Update predecessor with new successor"""
            reactor.connectTCP(self.dht.fingerTable.predecessor['ip'],
                               int(self.dht.fingerTable.predecessor['port']), DHTSuccessorUpdate(incomingDHT))


            reactor.connectTCP(incomingDHT['ip'], int(incomingDHT['port']), DHTReturn(dhtForNewNode.fingerTable.toDict()))

            self.dht.fingerTable.predecessor = incomingDHT
            self.dht.writeDHTInformation()

        elif(incomingDHT['nodeid'] > self.dht.fingerTable.nodeid['nodeid']):
            print("New Successor NO EDGE CASE")

            dhtForNewNode = Initialization()
            dhtForNewNode.fingerTable.successor = self.dht.fingerTable.successor
            dhtForNewNode.fingerTable.nodeid = incomingDHT
            dhtForNewNode.fingerTable.predecessor = self.dht.fingerTable.nodeid

            """Update Successor with new predecessor"""
            reactor.connectTCP(self.dht.fingerTable.successor['ip'],
                               int(self.dht.fingerTable.successor['port']), DHTPredecessorUpdate(incomingDHT))

            reactor.connectTCP(incomingDHT['ip'], int(incomingDHT['port']), DHTReturn(dhtForNewNode.fingerTable.toDict()))

            print(str(incomingDHT['ip'] + incomingDHT['port']))
            self.dht.fingerTable.successor = incomingDHT
            self.dht.writeDHTInformation()

        elif(incomingDHT['nodeid'] > self.dht.fingerTable.successor['nodeid']):
            print("Send to next node")
            reactor.connectTCP(self.dht.fingerTable.successor['ip'],
                               int(self.dht.fingerTable.successor['port']), DHTFactory(incomingDHT))

        elif(incomingDHT['nodeid'] < self.dht.fingerTable.predecessor['nodeid']):
            print("Send to previous node")
            reactor.connectTCP(self.dht.fingerTable.predecessor['ip'],
                               int(self.dht.fingerTable.predecessor['port']), DHTFactory(incomingDHT))

        else:
            print("fuck you")

        print("suptoad")

    def DHTInformationSearch(self, userSearchRequest):
        print("DHT Informatiom Search")
        """Should send just a hash value of the user they are interested in finding"""
        userSearchRequest = userSearchRequest.replace("==DHTSEARCH==", "")
        print(userSearchRequest)
        self.dht.loadDHTInformation()
        userSearchRequest = ast.literal_eval(userSearchRequest)


        if(self.dht.fingerTable.successor['nodeid'] == userSearchRequest['username']):
            print("Found user returning object succ")
            userfound = self.dht.fingerTable.successor
            reactor.connectTCP(userSearchRequest['ip'],
                               int(userSearchRequest['port']), DHTSearchReturn(userfound))
        elif(self.dht.fingerTable.predecessor['nodeid'] == userSearchRequest['username']):
            print("Found user returning object precc")
            userfound = self.dht.fingerTable.predecessor
            reactor.connectTCP(userSearchRequest['ip'],
                               int(userSearchRequest['port']), DHTSearchReturn(userfound))

        elif(self.dht.fingerTable.nodeid['nodeid'] == userSearchRequest['username']):
            print("Found user is my node ID!")
            userfound = self.dht.fingerTable.nodeid
            reactor.connectTCP(userSearchRequest['ip'],
                                   int(userSearchRequest['port']), DHTSearchReturn(userfound))

        elif(userSearchRequest['username'] > self.dht.fingerTable.successor['nodeid']):
            print("Move foward!")
            reactor.connectTCP(self.dht.fingerTable.successor['ip'], int(self.dht.fingerTable.successor['port']),
                               DHTSearch(userSearchRequest))
        elif(userSearchRequest['username'] < self.dht.fingerTable.predecessor['nodeid']):
            print("Move backward")
            reactor.connectTCP(self.dht.fingerTable.predecessor['ip'], int(self.dht.fingerTable.predecessor['port']),
                               DHTSearch(userSearchRequest))
        else:
            print("Something invalid")





