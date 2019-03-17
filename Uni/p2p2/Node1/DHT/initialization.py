import json
from twisted.internet import reactor
from Node1.Client.DHTPredecessorUpdate import DHTPredecessorUpdate
from Node1.Client.DHTSuccessorUpdate import DHTSuccessorUpdate
from Node1.Client.RegisterFactory import MessageCFactory
from Node1.Models.FingerTable import FingerTable
import logging


class Initialization():

    fingerTable = FingerTable


    def loadDHTInformation(self):
        dhtfile = open("DHT.json", "r")
        dhtfile = dhtfile.read()
        dhtfile = json.loads(dhtfile)

        print(type(dhtfile))


        self.fingerTable.successor = dhtfile['successor']
        self.fingerTable.predecessor = dhtfile['predecessor']
        self.fingerTable.nodeid = dhtfile['nodeid']

    def writeDHTInformation(self):

        """Write our DHT information to file once its been generated and we have established who are successor and predecessor are"""
        file = open("DHT.json", "w+")
        print(self.fingerTable.toDict())
        dhtinfo = json.dumps((self.fingerTable.toDict()))
        file.write(dhtinfo)
        file.flush()


    def __init__(self):
        print("in init")
        self.fingerTable = FingerTable()


