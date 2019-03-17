import collections
import hashlib
import itertools
import json
import random
import socket
from time import sleep

from twisted.internet import reactor

from Node1.Client.DHTPredecessorUpdate import DHTPredecessorUpdate
from Node1.Client.DHTSuccessorUpdate import DHTSuccessorUpdate
from Node1.Client.RegisterFactory import MessageCFactory
from Node1.Models.FingerTable import FingerTable


class Initialization():

    fingerTable = FingerTable


    def checkWhereKeyBelongs(self, transport, newKey, predecessor, localNodeKey, successor):
        """Key1: New key that we are comparing and wish to find where it resides"""
        """Key2 Nodes predessor key"""
        """Key3 Nodes key"""
        """Key4 Nodes successor key"""
        self.loadDHTInformation()
        print(newKey)
        print(predecessor)
        print(localNodeKey)
        print(successor)

        if(newKey['nodeid'] > successor['nodeid']):
            print("Keep moving foward away from this node")
            CMD = '==REGISTER=='
            foward = CMD + newKey
            foward = str(foward)
            foward = foward.encode('utf-8')

            reactor.connectTCP(self.dht.fingerTable.successor['ip'],
                           int(self.dht.fingerTable.successor['port']), MessageCFactory(foward))

        elif(newKey['nodeid'] > localNodeKey['nodeid']):
            """This means the key is greater than this node but not greater than its successor making it the new successor of this node"""
            print("New Successor found for this node")
            self.fingerTable.successor = newKey
            reactor.connectTCP(self.dht.fingerTable.successor['ip'],
                               int(self.dht.fingerTable.successor['port']), DHTPredecessorUpdate(newKey))


        elif(newKey[['nodeid']] > predecessor['nodeid']):
            """This means the key is greater than this node but not greater than its precdessor making it the new precdessor of this node"""
            print("New Predecessor found for this node")
            self.fingerTable.predecessor = newKey
            reactor.connectTCP(self.dht.fingerTable.predecessor['ip'],
                               int(self.dht.fingerTable.predecessor['port']), DHTSuccessorUpdate(newKey))

        elif(newKey['nodeid'] < predecessor['nodeid']):
            """This means the key is less than the precdessor meaning it has no relvance to this node and we should move backwards through the linked list"""
            print("Start moving backwards")
            CMD = '==REGISTER=='
            foward = CMD + newKey
            foward = str(foward)
            foward = foward.encode('utf-8')

            reactor.connectTCP(self.dht.fingerTable.predecessor['ip'],
                               int(self.dht.fingerTable.predecessor['port']), MessageCFactory(foward))

        else:
            print("Same key, CONFLICT?!")

    def isBetween(self, key1, key2):
        print("")


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


